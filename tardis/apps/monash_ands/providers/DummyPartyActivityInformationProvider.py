import logging
from django.conf import settings
import urllib2
from tardis.apps.monash_ands.PartyActivityInformationProvider \
    import PartyActivityInformationProvider
from xml.dom.minidom import parseString

logger = logging.getLogger(__name__)

class DummyPartyActivityInformationProvider(PartyActivityInformationProvider):

    name = u'Dummy EIF038 Web Services'

    def get_unique_party_id(self, username):
        """
        return the user dictionary in the format of::

        """

        return username[:3] + str(45)

    def get_party_rifcs(self, unique_party_id):
        """
        return the user dictionary in the format of::


        """
        party_url = settings.TEST_MONASH_ANDS_URL\
        + "pilot/GetPartybyMonashID/"

        requestmp = urllib2.Request(party_url)
        party_rif_cs = urllib2.urlopen(requestmp).read()
        return party_rif_cs

    def get_display_name_for_party(self, unique_party_id):
        """
        return the user dictionary in the format of::


        """
        party_rif_cs = self.get_party_rifcs(unique_party_id)

        from lxml import etree
        import StringIO

        rif_tree = etree.parse(StringIO.StringIO(party_rif_cs))
        title = rif_tree.xpath('//name/namePart[@type="title"]/text()')[0]
        given = rif_tree.xpath('//name/namePart[@type="given"]/text()')[0]
        family = rif_tree.xpath('//name/namePart[@type="family"]/text()')[0]

        return title + " " + given + " " + family

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
            activity['projectId'] = grant_id

            title=node.getElementsByTagName('title')[0].\
            childNodes[0].nodeValue
            activity['projectTitle'] = title

            funding_body=node.getElementsByTagName('funding_body')[0].\
            childNodes[0].nodeValue
            activity['grantorCode'] = funding_body

            description=node.getElementsByTagName('description')[0].\
            childNodes[0].nodeValue
            activity['projectDateApplied'] = description

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
