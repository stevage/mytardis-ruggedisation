'''

'''
from tardis.tardis_portal.ParameterSetManager import\
    ParameterSetManager
from tardis.tardis_portal.models import \
    Experiment, ExperimentParameterSet

class CreativeCommonsHandler():

    psm = None
    schema = "http://www.tardis.edu.au/schemas" +\
    "/creative_commons/2011/05/17"
    experiment_id = None

    def __init__(self, experiment_id=experiment_id, create=True):

        self.experiment_id = experiment_id

        if create:
            self.psm = self.get_or_create_cc_parameterset(create=True)
        else:
            self.psm = self.get_or_create_cc_parameterset(create=False)

    def get_or_create_cc_parameterset(self, create=True):

        # get cc license parameterset, if any
        parameterset = ExperimentParameterSet.objects.filter(
        schema__namespace=self.schema,
        experiment__id=self.experiment_id)

        if not len(parameterset):
            if create:
                experiment = Experiment.objects.get(id=self.experiment_id)
                self.psm = ParameterSetManager(schema=self.schema,
                        parentObject=experiment)
            else:
                return None
        else:
            self.psm = ParameterSetManager(parameterset=parameterset[0])

        return self.psm

    def has_cc_license(self):

        # get cc license parameterset, if any

        parameterset = ExperimentParameterSet.objects.filter(
        schema__namespace=self.schema,
        experiment__id=self.experiment_id)

        self.psm = None
        if not len(parameterset):
            return False
        else:
            return True

    def save_license(self, request):
            # if cc license then save params
        if request.POST['cc_js_want_cc_license'] ==\
            'sure':
            cc_js_result_img = request.POST['cc_js_result_img']
            cc_js_result_name = request.POST['cc_js_result_name']
            cc_js_result_uri = request.POST['cc_js_result_uri']

            self.psm.set_param("license_image", cc_js_result_img,
                "License Image")
            self.psm.set_param("license_name", cc_js_result_name,
                "License Name")
            self.psm.set_param("license_uri", cc_js_result_uri,
                "License URI")
        else:
            self.psm.delete_params('license_image')
            self.psm.delete_params('license_name')
            self.psm.delete_params('license_uri')

            parametersets = ExperimentParameterSet.objects.filter(
            schema__namespace=self.schema,
            experiment__id=self.experiment_id)

            for parameterset in parametersets:
                parameterset.delete()