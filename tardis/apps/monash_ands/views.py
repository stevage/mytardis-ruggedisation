# -*- coding: utf-8 -*-

from django.http import HttpResponse
#from django.template import Context

from tardis.tardis_portal.shortcuts import render_response_index
from MonashANDSService import MonashANDSService

def index(request, experiment_id):

    monashandsService = MonashANDSService(experiment_id)
    c = monashandsService.get_context(request)
    url = 'monash_ands/form.html'
    return HttpResponse(render_response_index(request, url, c))
