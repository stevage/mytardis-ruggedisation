import logging
from django.conf import settings
import urllib2
from tardis.tardis_portal.\
    PartyActivityInformationProvider import PartyActivityInformationProvider
from xml.dom.minidom import parseString

logger = logging.getLogger(__name__)

class DummyPartyActivityInformationProvider(PartyActivityInformationProvider):

    name = u'Dummy EIF038 Web Services'

    def get_unique_party_id(self, username):
        """
        return the user dictionary in the format of::

        """
        monash_id_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetMonashIDbyAuthcate/" + username

        requestmp = urllib2.Request(monash_id_url)

        monash_id = urllib2.urlopen(requestmp).read()

        return monash_id

    def get_party_rifcs(self, unique_party_id):
        """
        return the user dictionary in the format of::


        """
        party_url = settings.TEST_MONASH_ANDS_URL\
        + "pilot/GetPartybyMonashID/"

        requestmp = urllib2.Request(party_url)
        party_rif_cs = urllib2.urlopen(requestmp).read()
        return party_rif_cs

    def get_activity_summary_dict(self, username):
        """
        return the user dictionary in the format of::


        """
        activity_url = settings.TEST_MONASH_ANDS_URL + \
        "pilot/GetActivitySummarybyMonashID/" + username + "/"

        requestmp = urllib2.Request(activity_url)

        doc_string = urllib2.urlopen(requestmp).read()

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

        return activities


    def get_activity_rifcs(self, activity_id):
        """
        return the user dictionary in the format of::


        """
        activity_url = settings.TEST_MONASH_ANDS_URL\
        + "pilot/GetActivitybyGrantID/"

        requestmp = urllib2.Request(activity_url)
        activity_rif_cs = urllib2.urlopen(requestmp).read()

        return activity_rif_cs
