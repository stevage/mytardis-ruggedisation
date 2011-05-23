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

        filename = settings.OAI_DOCS_PATH + path.sep + "rif" + \
            path.sep + str(objectprefix) + "-" + str(uniqueid) + ".xml"

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

        filename = settings.OAI_DOCS_PATH + path.sep + "rif" + \
            path.sep + str(objectprefix) + "-" + \
            str(uniqueid) + ".xml"

        f = open(filename, "w")

        f.write(xmlstring)
        f.close()
        return filename
