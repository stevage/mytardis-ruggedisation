'''
Local DB Authentication module.

.. moduleauthor:: Gerson Galang <gerson.galang@versi.edu.au>
'''
from tardis.tardis_portal.logger import logger
from tardis.tardis_portal.publish.interfaces import PublishProvider

class MonashANDSPublishProvider(PublishProvider):
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
    
    name = u'Monash ANDS Publisher'
    
    def execute_publish(self, request):
        """
        return the user dictionary in the format of::
            
            {"id": 123,
            "display": "John Smith",
            "email": "john@example.com"}
        
        """
        # userObj = User.objects.get(id=id)
        # if userObj:
        #     return {'id': id, 'display': userObj.first_name + ' ' +
        #         userObj.last_name, 'email': userObj.email}
        return {'status': True, 'message': 'Success'}
    
    def get_template_path(self):
        """
        return a list of user descriptions from the auth domain.
        
        each user is in the format of::
            
            {"id": 123,
            "display": "John Smith",
            "email": "john@example.com"}
        
        """
        return self.name + "/form.html"