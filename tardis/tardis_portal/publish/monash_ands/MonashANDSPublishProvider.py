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

class MonashANDSPublishProvider(PublishProvider):
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
    
    name = u'Monash ANDS Publish'
    
    def execute_publish(self, request):
        """
        return the user dictionary in the format of::
            
            {"id": 123,
            "display": "John Smith",
            "email": "john@example.com"}
        
        """
        experiment = Experiment.objects.get(id=self.experiment_id)
        
        monash_id_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetMonashIDbyAuthcate/" + request.user.username
        
        requestmp = urllib2.Request(monash_id_url)
        monash_id = urllib2.urlopen(requestmp).read()
        
        self.save_party_parameter(experiment, monash_id)
        
        if request.POST['parties']:
            for authcate in request.POST['parties'].split(","):
                
                monash_id_url = settings.TEST_MONASH_ANDS_URL + \
                "pilot/GetMonashIDbyAuthcate/" + str(authcate.strip())
                
                requestmp = urllib2.Request(monash_id_url)
                monash_id = urllib2.urlopen(requestmp).read()
                
                self.save_party_parameter(experiment, monash_id)
        
        for activity_id in request.POST.getlist('activity'):
            self.save_activity_parameter(experiment, activity_id)
        
        profile = request.POST['profile']
        self.save_rif_cs_profile(experiment, profile)
        
        return {'status': True, 'message': 'Success'}
    
    def get_context(self, request):
        
        """
        """
        
        from xml.dom.minidom import parse, parseString
        
        monash_id_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetMonashIDbyAuthcate/" + request.user.username
        
        requestmp = urllib2.Request(monash_id_url)
        monash_id = urllib2.urlopen(requestmp).read()
        
        activity_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetActivitySummarybyMonashID/" + monash_id + "/"
        
        print activity_url
        
        requestmp = urllib2.Request(activity_url)
        doc_string = urllib2.urlopen(requestmp).read()
        
        dom = parseString(doc_string)
        doc = dom.documentElement
        
        activity_summary=dom.getElementsByTagName('activity_summary')
        activities = []
        for node in activity_summary:
            
            activity = {}
            
            grant_id=node.getElementsByTagName('grant_id')[0].childNodes[0].nodeValue
            
            activity['grant_id'] = grant_id
            
            title=node.getElementsByTagName('title')[0].childNodes[0].nodeValue
            activity['title'] = title
            
            funding_body=node.getElementsByTagName('funding_body')[0].childNodes[0].nodeValue
            activity['funding_body'] = funding_body
            
            description=node.getElementsByTagName('description')[0].childNodes[0].nodeValue
            activity['description'] = description
            
            memberList = []
            members=node.getElementsByTagName('members')[0].getElementsByTagName('member')
            
            for m in members:
                membertext = m.childNodes[0].nodeValue
                memberList.append(membertext)
            
            activity['members'] = memberList
            
            activities.append(activity)
        
        return {"activities": activities}
    
    def get_path(self):
        """
        get path
        """
        return "monash_ands/form.html"
    
    def save_party_parameter(self, experiment, monash_id):
        # save party experiment parameter
        
        schema = \
            Schema.objects.get(
            namespace__exact="http://localhost/pilot/party/1.0/")
        
        parametername = \
            ParameterName.objects.get(
            schema__namespace__exact=schema.namespace,
            name="party_id")
        
        try:
            parameterset = ExperimentParameterSet.objects.get(schema=schema, \
            experiment=experiment)
        except ExperimentParameterSet.DoesNotExist, e:
            parameterset = \
                ExperimentParameterSet(
                schema=schema, experiment=experiment)
            
            parameterset.save()
        
        ep = ExperimentParameter(
            parameterset=parameterset,
            name=parametername,
            string_value=monash_id,
            numerical_value=None)
        ep.save()
    
    def save_activity_parameter(self, experiment, activity_id):
        # save party experiment parameter
        
        schema = \
            Schema.objects.get(
            namespace__exact="http://localhost/pilot/activity/1.0/")
        
        parametername = \
            ParameterName.objects.get(
            schema__namespace__exact=schema.namespace,
            name="activity_id")
        
        try:
            parameterset = ExperimentParameterSet.objects.get(schema=schema, \
            experiment=experiment)
        except ExperimentParameterSet.DoesNotExist, e:
            parameterset = \
                ExperimentParameterSet(
                schema=schema, experiment=experiment)
            
            parameterset.save()
        
        ep = ExperimentParameter(
            parameterset=parameterset,
            name=parametername,
            string_value=activity_id,
            numerical_value=None)
        ep.save()
    
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