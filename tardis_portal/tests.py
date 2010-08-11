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

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


# http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
class UrlTest(TestCase):
    def test_root(self):
        self.failUnlessEqual(Client().get('/').status_code, 200)

    def test_urls(self):
        c = Client()
        urls  = ['/login', '/about', '/partners', '/stats']
        urls += ['/experiment/register', '/experiment/view']
        urls += ['/search/experiment', '/search/datafile']

        for u in urls:
            response = c.get(u)
            # print u, response.status_code
            self.failUnlessEqual(response.status_code, 301)


class RegisterExperiment(TestCase):
    def test_register(self):
        self.client = Client()

        from django.contrib.auth.models import User
        user='user1'
        pwd='test'
        email=''
        User.objects.create_user(user, email, pwd)

        f = open('tardis_portal/tests/notMETS_test.xml')
        response = self.client.post('/experiment/register/', {'username': user,
                                                              'password': pwd,
                                                              'xmldata': f,
                                                              'originid': '286',
                                                              'experiment_owner': user})
        f.close()
        self.failUnlessEqual(response.status_code, 200)
    
    
class LoginTest(TestCase):
    def test_login(self):
        from django.contrib.auth.models import User
        user='user2'
        pwd='test'
        email=''
        User.objects.create_user(user, email, pwd)

        self.failUnlessEqual(self.client.login(username=user, password=pwd), True)        
        
