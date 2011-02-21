'''
Local DB Authentication module.

.. moduleauthor:: Gerson Galang <gerson.galang@versi.edu.au>
'''
from tardis.tardis_portal.logger import logger
from tardis.tardis_portal.publish.interfaces import PublishProvider
from tardis.tardis_portal.models import Experiment

class DefaultPublishProvider(PublishProvider):
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
    
    name = u'MyTARDIS Publish'
    
    def execute_publish(self, request):
        """
        return the user dictionary in the format of::
            
            {"id": 123,
            "display": "John Smith",
            "email": "john@example.com"}
        
        """
        
        if request.method == 'POST':
            if 'legal' in request.POST:
                experiment = Experiment.objects.get(id=self.experiment_id)
                experiment.public = True
                experiment.save()
                return {'status': True, 'message': 'Experiment Public'}
            else:
                return {'status': False, 'message': 'Please accept the legal agreement'}
        
        # userObj = User.objects.get(id=id)
        # if userObj:
        #     return {'id': id, 'display': userObj.first_name + ' ' +
        #         userObj.last_name, 'email': userObj.email}
        return {'status': False, 'message': 'Unknown error'}
    
    def get_template_path(self):
        
        print "PUB EXP: " + str(self.experiment_id)
        """
        return a list of user descriptions from the auth domain.
        
        each user is in the format of::
            
            {"id": 123,
            "display": "John Smith",
            "email": "john@example.com"}
        
        """
        return "default/form.html"