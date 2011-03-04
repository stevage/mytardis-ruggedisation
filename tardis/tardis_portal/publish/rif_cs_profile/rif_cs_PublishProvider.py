'''
Local DB Authentication module.

.. moduleauthor:: Gerson Galang <gerson.galang@versi.edu.au>
'''
from tardis.tardis_portal.logger import logger
from tardis.tardis_portal.publish.interfaces import PublishProvider
from django.conf import settings
from tardis.tardis_portal.models import Experiment, ExperimentParameter, \
    ParameterName, Schema, ExperimentParameterSet
import urllib2
from urllib import urlencode, unquote_plus, urlopen
import os

class rif_cs_PublishProvider(PublishProvider):
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
    
    name = u'Research Data Australia Profile'
    
    def execute_publish(self, request):
        """
        return the user dictionary in the format of::
            
            {"id": 123,
            "display": "John Smith",
            "email": "john@example.com"}
        
        """
        if request.POST['profile']:
            experiment = Experiment.objects.get(id=self.experiment_id)
            
            profile = request.POST['profile']
            self.save_rif_cs_profile(experiment, profile)
            
            return {'status': True, 'message': 'Success'}
        else:
            return {'status': False, 'message': 'Profile Selection Not Detected'}
    
    
    def get_context(self, request):
        
        """
        """
        
        rif_cs_profiles = self.get_rif_cs_profile_list()
        
        return {"rif_cs_profiles": rif_cs_profiles}
    
    
    def get_path(self):
        """
        get path
        """
        return "rif_cs_profile/form.html"
    
    
    def get_rif_cs_profile_list(self):
        """
        Return a list of the possible RIF-CS profiles that can
        be applied.
        
        :rtype: list of strings
        """
        
        # TODO this is not a scalable or pluggable way of listing
        #  or defining RIF-CS profiles. The current method REQUIRES
        #  branching of the templates directory. instead of using the
        #  built in template resolution tools.
        TARDIS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        profile_dir = os.path.join(TARDIS_ROOT,
                      "profiles/")
        
        profile_list = list()
        
        for f in os.listdir(profile_dir):
            if not os.path.isfile(profile_dir + f) or \
                   f.startswith('.') or not f.endswith('.xml'):
                continue
            profile_list.append(f)
        
        return profile_list
    
    
    def save_rif_cs_profile(self, experiment, profile):
        # save party experiment parameter
        
        schema = Schema.objects.get(
            namespace__exact="http://monash.edu.au/rif-cs/profile/")
        
        parametername = ParameterName.objects.get(
            schema__namespace__exact=schema.namespace,
            name="profile")
        
        try:
            parameterset = \
                         ExperimentParameterSet.objects.get(schema=schema,
                                                            experiment=experiment)
        except ExperimentParameterSet.DoesNotExist, e:
            parameterset = ExperimentParameterSet(schema=schema,
                                                  experiment=experiment)
            
            parameterset.save()
        
        ep = ExperimentParameter(
            parameterset=parameterset,
            name=parametername,
            string_value=profile,
            numerical_value=None)
        ep.save()
    
    
    def get_profile(self):
        """
        get existing rif-cs profile for experiment, if any
        """
        
        ep = ExperimentParameter.objects.filter(name__name='profile',
        parameterset__schema__namespace='http://monash.edu.au/rif-cs/profile/',
        parameterset__experiment__id=self.experiment_id)
        
        if len(ep):
            return ep[0].string_value
        else:
            return None