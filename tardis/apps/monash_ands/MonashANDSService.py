'''
Monash ANDS Publish Provider (Research Master Interaction)

.. moduleauthor:: Steve Androulakis <steve.androulakis@monash.edu>
'''
from tardis.tardis_portal.logger import logger
from django.conf import settings
from django.template import Context
from tardis.tardis_portal.models import Experiment, ExperimentParameter, \
    ParameterName, Schema, ExperimentParameterSet
import urllib2
import datetime
from tardis.tardis_portal.partyactivityinformationservice \
    import PartyActivityInformationService
from tardis.tardis_portal.oaipmhservice \
    import OAIPMHService


class MonashANDSService():

    def __init__(self, experiment_id):
        self.experiment_id = experiment_id

    name = u'Monash ANDS Publish'

    def register(self, request):
        """
        Use the EIF038 web services to gather and store party/activity
        ids for the linkages required by ANDS Research Data Australia.

        :param request: a HTTP Request instance
        :type request: :class:`django.http.HttpRequest`

        """
        username = request.user.username
        pais = PartyActivityInformationService()
        pai = pais.get_pai()

        party_list = request.POST.getlist('ldap_existing_party')

        experiment = Experiment.objects.get(id=self.experiment_id)

        self.clear_existing_parameters(request)

        if 'ldap_party' in request.POST:
            for authcate in request.POST.getlist('ldap_party'):

                if str(authcate.strip()):

                    monash_id = ""
                    try:
                        monash_id = pai.get_unique_party_id(str(authcate.strip()))
                    except urllib2.URLError:
                        logger.error("Can't contact research" +
                            " master web service")

                        return {'status': False,
                        'message': 'Error: Cannot contact Activity' +
                        ' / Party Service. Please try again later.'}

                    party_list.append(monash_id)
                    self.save_party_parameter(experiment, monash_id)

                    if settings.OAI_DOCS_PATH:
                        party_rif_cs = pai.get_party_rifcs("")

                        OAIPMHService.write_xml_to_file(
                            'rif',
                            'party',
                            monash_id,
                            party_rif_cs
                            )

        if 'freeform_party' in request.POST:
            for party in request.POST.getlist('freeform_party'):

                if str(party.strip()):

                    party_key = self.save_party_parameter(experiment,
                        party, freeform=True)
                    party_list.append(party_key)

                    if settings.OAI_DOCS_PATH:
                        c = Context({
                                    'party_key': party_key,
                                    'party': party.strip(),
                                    })

                        OAIPMHService.write_freeform_party_file(
                            'rif',
                            party_key,
                            'monash_ands/party.xml',
                            c,
                            )


        for activity_id in request.POST.getlist('activity'):
            self.save_activity_parameter(experiment, activity_id)

            if settings.OAI_DOCS_PATH:
                activity_rif_cs = pai.get_activity_rifcs("")

                OAIPMHService.write_xml_to_file(
                    'rif',
                    'activity',
                    activity_id,
                    activity_rif_cs
                    )

        c = Context({
                    'now': datetime.datetime.now(),
                    'experiment': experiment,
                    'party_keys': party_list,
                    'activity_keys': request.POST.getlist('activity'),
                    })


        if settings.OAI_DOCS_PATH:
            OAIPMHService.write_collection_file(
                'rif',
                experiment.id,
                experiment.profile(),
                c,
                )

        return {'status': True, 'message': 'Success'}

    def get_context(self, request):
        """
        Use the logged in username to get a list of activity summaries from
        Research Master and display them on screen for selection.

        :param request: a HTTP Request instance
        :type request: :class:`django.http.HttpRequest`

        """
        username = request.user.username
        pais = PartyActivityInformationService()
        pai = pais.get_pai()
        # already has entries

        monash_id = ""
        try:
            monash_id = pai.get_unique_party_id(username)
        except urllib2.URLError:
            logger.error("Can't contact research master web service")
            return {'message':
            'Error: Failed to contact Research Master web service ' +
            'to retrieve Party / Activity information. Please contact ' +
            'a system administrator.'}

        activity_summaries = {}
        try:
            activity_summaries = pai.get_activity_summary_dict("username")
        except urllib2.URLError:
            logger.error("Can't contact research master web service")
            return {'message':
            'Error: Failed to contact Research Master web service ' +
            'to retrieve Party / Activity information. Please contact ' +
            'a system administrator.'}

        return {"activity_summaries":
                    activity_summaries,
                "current_activities":
                    self.get_existing_activity_keys(),
                "current_parties_ldap":
                    self.get_existing_ldap_party_keys(),
                "current_parties_freeform":
                    self.get_existing_freeform_party_keys(),
                }

    def save_party_parameter(self, experiment, party_param, freeform=False):
        """
        Save Research Master's returned Party ID as an experiment parameter
        """
        namespace = "http://localhost/pilot/party/1.0/"

        parameter_name = 'party_id'
        if freeform:
            parameter_name = 'party_string'

        schema = None
        try:
            schema = Schema.objects.get(
                namespace__exact=namespace)
        except Schema.DoesNotExist:
            logger.debug('Schema ' + namespace +
            ' does not exist. Creating.')
            schema = Schema(namespace=namespace)
            schema.save()

        parametername = \
            ParameterName.objects.get(
            schema__namespace__exact=schema.namespace,
            name=parameter_name)

        try:
            parameterset = ExperimentParameterSet.objects.get(schema=schema, \
            experiment=experiment)

        except ExperimentParameterSet.DoesNotExist, e:
            parameterset = \
                ExperimentParameterSet(
                schema=schema, experiment=experiment)

            parameterset.save()

        eps = ExperimentParameter.objects.filter(name__name=parameter_name,
        parameterset__schema__namespace=namespace,
        parameterset__experiment__id=self.experiment_id,
        string_value=party_param)

        if not len(eps):
            ep = ExperimentParameter(
                parameterset=parameterset,
                name=parametername,
                string_value=party_param,
                numerical_value=None)
            ep.save()
        else:
            ep = eps[0]

        return ep.id

    def save_activity_parameter(self, experiment, activity_id):
        """
        Save Research Master's returned Activity ID as an experiment parameter
        """
        namespace = "http://localhost/pilot/activity/1.0/"
        schema = None
        try:
            schema = Schema.objects.get(
                namespace__exact=namespace)
        except Schema.DoesNotExist:
            logger.debug('Schema ' + namespace +
            ' does not exist. Creating.')
            schema = Schema(namespace=namespace)
            schema.save()

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

        ep = ExperimentParameter.objects.filter(name__name='activity_id',
        parameterset__schema__namespace=namespace,
        parameterset__experiment__id=self.experiment_id,
        string_value=activity_id)

        if not len(ep):
            ep = ExperimentParameter(
                parameterset=parameterset,
                name=parametername,
                string_value=activity_id,
                numerical_value=None)
            ep.save()

    def clear_existing_parameters(self, request):
        """
        Clear existing party/activity keys
        """
        for e_param in self.get_existing_ldap_party_keys():
            if  not e_param.string_value in\
                request.POST.getlist('ldap_existing_party'):

                e_param.delete()

        for e_param in self.get_existing_freeform_party_keys():
            if  not e_param.string_value in\
                request.POST.getlist('freeform_party'):

                e_param.delete()


        for e_param in self.get_existing_activity_keys():
            if  not e_param.string_value in\
                request.POST.getlist('activity'):
                e_param.delete()

    def get_existing_ldap_party_keys(self):
        eps = ExperimentParameter.objects.filter(name__name='party_id',
        parameterset__schema__namespace='http://localhost/pilot/party/1.0/',
        parameterset__experiment__id=self.experiment_id)

        return eps

    def get_existing_freeform_party_keys(self):
        eps = ExperimentParameter.objects.filter(name__name='party_string',
        parameterset__schema__namespace='http://localhost/pilot/party/1.0/',
        parameterset__experiment__id=self.experiment_id)

        return eps

    def get_existing_activity_keys(self):
        eps = ExperimentParameter.objects.filter(name__name='activity_id',
        parameterset__schema__namespace='http://localhost/pilot/activity/1.0/',
        parameterset__experiment__id=self.experiment_id)

        return eps
