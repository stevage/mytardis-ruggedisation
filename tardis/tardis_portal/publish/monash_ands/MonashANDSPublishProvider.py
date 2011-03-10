'''
Monash ANDS Publish Provider (Research Master Interaction)

.. moduleauthor:: Steve Androulakis <steve.androulakis@monash.edu>
'''
#from tardis.tardis_portal.logger import logger
from tardis.tardis_portal.publish.interfaces import PublishProvider
from django.conf import settings
from tardis.tardis_portal.models import Experiment, ExperimentParameter, \
    ParameterName, Schema, ExperimentParameterSet
import urllib2


class MonashANDSPublishProvider(PublishProvider):

    def __init__(self, experiment_id):
        self.experiment_id = experiment_id

    name = u'Monash ANDS Publish'

    def execute_publish(self, request):
        """
        Use the EIF038 web services to gather and store party/activity
        ids for the linkages required by ANDS Research Data Australia.

        :param request: a HTTP Request instance
        :type request: :class:`django.http.HttpRequest`

        """
        if self.has_parameters():
            return {'status': True,
                'message': 'Party and Activity IDs Already Set'}

        experiment = Experiment.objects.get(id=self.experiment_id)

        monash_id_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetMonashIDbyAuthcate/" + request.user.username

        requestmp = urllib2.Request(monash_id_url)

        try:
            monash_id = urllib2.urlopen(requestmp).read()
        except urllib2.URLError:
            return {'status': False,
            'message': 'Error: Cannot contact Activity / Party Service.' +
            ' Please try again later.'}

        self.save_party_parameter(experiment, monash_id)

        if 'parties' in request.POST:
            for authcate in request.POST['parties'].split(","):

                monash_id_url = settings.TEST_MONASH_ANDS_URL + \
                "pilot/GetMonashIDbyAuthcate/" + str(authcate.strip())

                requestmp = urllib2.Request(monash_id_url)

                try:
                    monash_id = urllib2.urlopen(requestmp).read()
                except urllib2.URLError:
                    return {'status': False,
                    'message': 'Error: Cannot contact Activity' +
                    ' / Party Service. Please try again later.'}

                self.save_party_parameter(experiment, monash_id)

        for activity_id in request.POST.getlist('activity'):
            self.save_activity_parameter(experiment, activity_id)

        return {'status': True, 'message': 'Success'}

    def get_context(self, request):
        """
        Use the logged in username to get a list of activity summaries from
        Research Master and display them on screen for selection.

        :param request: a HTTP Request instance
        :type request: :class:`django.http.HttpRequest`

        """
        # already has entries
        if self.has_parameters():
            return {'message':
            'There are already party and activity ' +
            'entries for this experiment.'}

        from xml.dom.minidom import parseString

        monash_id_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetMonashIDbyAuthcate/" + request.user.username

        requestmp = urllib2.Request(monash_id_url)

        try:
            monash_id = urllib2.urlopen(requestmp).read()
        except urllib2.URLError:
            return {'message':
            'Error: Failed to contact Research Master web service ' +
            'to retrieve Party / Activity information. Please contact ' +
            'a system administrator.'}

        activity_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetActivitySummarybyMonashID/" + monash_id + "/"

        print activity_url

        requestmp = urllib2.Request(activity_url)
        try:
            doc_string = urllib2.urlopen(requestmp).read()
        except urllib2.URLError:
            return {'message':
            'Error: Failed to contact Research Master web service ' +
            'to retrieve Party / Activity information. Please contact ' +
            'a system administrator.'}

        dom = parseString(doc_string)
        doc = dom.documentElement

        activity_summary=dom.getElementsByTagName('activity_summary')
        activities = []
        for node in activity_summary:

            activity = {}

            grant_id=node.getElementsByTagName('grant_id')[0].\
            childNodes[0].nodeValue
            activity['grant_id'] = grant_id

            title=node.getElementsByTagName('title')[0].\
            childNodes[0].nodeValue
            activity['title'] = title

            funding_body=node.getElementsByTagName('funding_body')[0].\
            childNodes[0].nodeValue
            activity['funding_body'] = funding_body

            description=node.getElementsByTagName('description')[0].\
            childNodes[0].nodeValue
            activity['description'] = description

            activities.append(activity)

        return {"activities": activities}

    def get_path(self):
        """
        Return the relative template path for display
        """
        return "monash_ands/form.html"

    def save_party_parameter(self, experiment, monash_id):
        """
        Save Research Master's returned Party ID as an experiment parameter
        """
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
        """
        Save Research Master's returned Activity ID as an experiment parameter
        """

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

    def has_parameters(self):
        """
        Retrieve existing rif-cs profile for experiment, if any
        """

        ep = ExperimentParameter.objects.filter(name__name='party_id',
        parameterset__schema__namespace='http://localhost/pilot/party/1.0/',
        parameterset__experiment__id=self.experiment_id)

        if len(ep):
            return True

        ep = ExperimentParameter.objects.filter(name__name='activity_id',
        parameterset__schema__namespace='http://localhost/pilot/activity/1.0/',
        parameterset__experiment__id=self.experiment_id)

        if len(ep):
            return True

        return False
