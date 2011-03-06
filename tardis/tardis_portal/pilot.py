#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
pilot.py

@author Steve AndroulakisGetMonashIDbyAuthcate

"""

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from tardis.tardis_portal.models import *
from tardis.tardis_portal.logger import logger

# * = many
# dummy RESTful web service, in place of RM SOAP service
# * to *
def GetMonashIDbyAuthcate(request, authcate):
    
    # dummy functions for getting monash ID
    if authcate == "steveand":
        return HttpResponse('ste19234')
    else:
        import random
        
        rand = ""
        for i in range(5):
            rand = rand + str(random.randint(0, 9))
            
        monash_id = authcate[0:3] + rand
            
        return HttpResponse(monash_id)
        
# dummy RESTful web service, in place of RM SOAP service
# 1 to *
def GetActivitySummarybyMonashID(request, monash_id):

    if monash_id == "ste19234":
        c = Context({})
        return HttpResponse(render_response_index(request,
                            'tardis_portal/activity_summary.xml', c))
    else:
        return HttpResponse('Not Found')
        
# dummy RESTful web service, in place of RM SOAP service
# 1 to 1
def GetActivitybyGrantID(request):

    c = Context({})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/activity.xml', c))
        
# dummy RESTful web service, in place of RM SOAP service
# 1 to 1
def GetPartybyMonashID(request):
    
    c = Context({})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/party.xml', c))      