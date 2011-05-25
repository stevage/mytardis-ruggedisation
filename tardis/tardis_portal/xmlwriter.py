import logging
from django.conf import settings
from os import path
from tardis.tardis_portal.shortcuts import render_to_file

logger = logging.getLogger(__name__)

class XMLWriter:

    @staticmethod
    def write_template_to_file(metadataprefix,
        objectprefix,
        uniqueid,
        templatepath,
        context):

        uniqueid = str(uniqueid).replace('MON:', '')

        filename = settings.OAI_DOCS_PATH + path.sep + "rif" + \
            path.sep + str(objectprefix) + "-" + uniqueid + ".xml"

        render_to_file(templatepath,
            filename, context)

        return filename


    @staticmethod
    def write_xml_to_file(metadataprefix,
            objectprefix,
            uniqueid,
            xmlstring):
        """
        return the user dictionary in the format of::

        """
        uniqueid = str(uniqueid).replace('MON:', '')

        filename = settings.OAI_DOCS_PATH + path.sep + "rif" + \
            path.sep + str(objectprefix) + "-" + \
            uniqueid + ".xml"

        f = open(filename, "w")

        f.write(xmlstring.encode('UTF-8'))
        f.close()
        return filename
