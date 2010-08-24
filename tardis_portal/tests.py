#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010, Monash e-Research Centre
#   (Monash University, Australia)
# Copyright (c) 2010, VeRSI Consortium
#   (Victorian eResearch Strategic Initiative, Australia)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    *  Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    *  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    *  Neither the name of the VeRSI, the VeRSI Consortium members, nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# http://docs.djangoproject.com/en/dev/topics/testing/

from django.test import TestCase
from django.test.client import Client
import unittest


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """

        self.failUnlessEqual(1 + 1, 2)


# http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
class UserInterfaceTestCase(TestCase):

    def test_root(self):
        self.failUnlessEqual(Client().get('/').status_code, 200)

    def test_urls(self):
        c = Client()
        urls = ['/login', '/about', '/partners', '/stats']
        urls += ['/experiment/register', '/experiment/view']
        urls += ['/search/experiment', '/search/datafile']

        for u in urls:
            response = c.get(u)

            # print u, response.status_code

            self.failUnlessEqual(response.status_code, 301)

    def test_register(self):
        self.client = Client()

        from django.contrib.auth.models import User
        from tardis import settings
        import os

        user = 'user1'
        pwd = 'test'
        email = ''
        User.objects.create_user(user, email, pwd)

        f = open(os.path.join(settings.APP_ROOT,
                 'tardis_portal/tests/notMETS_test.xml'), 'r')
        response = self.client.post('/experiment/register/', {
            'username': user,
            'password': pwd,
            'xmldata': f,
            'originid': '286',
            'experiment_owner': user,
            })
        f.close()
        self.failUnlessEqual(response.status_code, 200)

    def test_login(self):
        from django.contrib.auth.models import User
        user = 'user2'
        pwd = 'test'
        email = ''
        User.objects.create_user(user, email, pwd)

        self.failUnlessEqual(self.client.login(username=user,
                             password=pwd), True)


class ExperimentParserTestCase(unittest.TestCase):

    def setUp(self):
        from tardis import settings
        import os
        f = open(os.path.join(settings.APP_ROOT,
                 'tardis_portal/tests/METS_test.xml'), 'r')
        xmlString = f.read()
        f.close()
        from tardis.tardis_portal.ExperimentParser import ExperimentParser
        self.experimentParser = ExperimentParser(str(xmlString))

    def testGetTitle(self):
        self.assertTrue(self.experimentParser.getTitle() == 'Test Title'
                        , 'title is not the same')

    def testGetAuthors(self):
        self.assertTrue(len(self.experimentParser.getAuthors()) == 3,
                        'number of authors should be 3')
        self.assertTrue('Author2'
                        in self.experimentParser.getAuthors(),
                        '"Author2 should be in the authors list"')

    def testGetAbstract(self):
        self.assertTrue(self.experimentParser.getAbstract()
                        == 'Test Abstract.', 'abstract is not the same')

    def testGetPDBIDs(self):
        self.assertTrue(len(self.experimentParser.getPDBIDs()) == 1,
                        'number of pdb ids should be 1')
        self.assertTrue('SAMPLE_PDBID'
                        in self.experimentParser.getPDBIDs(),
                        'pdb id should be "SAMPLE_PDBID"')

    def testGetRelationURLs(self):
        self.assertTrue('http://www.test.com'
                        in self.experimentParser.getRelationURLs(),
                        'missing url from relationsURLs')
        self.assertTrue(len(self.experimentParser.getRelationURLs())
                        == 1, 'there should only be 1 relationsURL')

    def testGetAgentName(self):
        self.assertTrue(self.experimentParser.getAgentName('CREATOR')
                        == 'Creator', 'agent should be "Creator"')
        self.assertTrue(self.experimentParser.getAgentName('PAINTER')
                        == None, 'there is no "Painter" agent')

    def testGetDatasetTitle(self):
        self.assertTrue(self.experimentParser.getDatasetTitle('J-2')
                        == 'Dataset1 Title',
                        'dataset title should be "J-2"')
        self.assertTrue(self.experimentParser.getDatasetTitle('J-4')
                        == None, 'there is no dataset with id "J-4"')

    def testGetDatasetDMDIDs(self):
        self.assertTrue(len(self.experimentParser.getDatasetDMDIDs())
                        == 2, 'total number of datasets is wrong')
        self.assertTrue('J-2'
                        in self.experimentParser.getDatasetDMDIDs(),
                        'J-2 is not in the dataset')
        self.assertTrue('J-1'
                        not in self.experimentParser.getDatasetDMDIDs(),
                        "J-1 shouldn't be in the dataset")

    def testGetDatasetADMIDs(self):

        # get metadata ids for this dataset...

        pass

    def testGetFileIDs(self):
        self.assertTrue('F-3' in self.experimentParser.getFileIDs('J-3'
                        ), 'F-3 is missing from the file IDs')
        self.assertTrue(len(self.experimentParser.getFileIDs('J-3'))
                        == 2,
                        'there should only be 2 files for the J-3 dataset'
                        )
        self.assertTrue('F-5'
                        not in self.experimentParser.getFileIDs('J-3'),
                        'F-3 is missing from the file IDs')

    def testGetFileLocation(self):
        self.assertTrue(self.experimentParser.getFileLocation('F-1')
                        == 'file://Images/File1',
                        "file F-1's location is wrong")

    def testGetFileADMIDs(self):

        # get metadata ids for this file...

        self.assertTrue('A-3'
                        in self.experimentParser.getFileADMIDs('F-4'),
                        'wrong file metadata id')
        self.assertTrue(len(self.experimentParser.getFileADMIDs('F-4'))
                        == 1,
                        'there should only be 1 metadata ID for the file'
                        )

    def testGetFileName(self):
        self.assertTrue(self.experimentParser.getFileName('F-1')
                        == 'File1', 'wrong file name for file "F-1"')

    def testGetFileSize(self):
        self.assertTrue(self.experimentParser.getFileSize('F-1')
                        == '6148', 'wrong file size for file "F-1"')

    def testGetTechXML(self):

        # check if the root of the returned element is datafile or something else

        self.assertTrue(self.experimentParser.getTechXML('A-3'
                        ).getroot().tag
                        == '{http://www.tardis.edu.au/schemas/trdDatafile/1}datafile'
                        , 'element has wrong tag')

    def testGetParameterFromTechXML(self):
        pass


def suite():
    userInterfaceSuite = \
        unittest.TestLoader().loadTestsFromTestCase(UserInterfaceTestCase)
    parserSuite = \
        unittest.TestLoader().loadTestsFromTestCase(ExperimentParserTestCase)
    allTests = unittest.TestSuite([parserSuite, userInterfaceSuite])
    return allTests


