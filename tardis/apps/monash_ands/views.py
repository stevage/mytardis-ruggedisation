# -*- coding: utf-8 -*-

from django.http import HttpResponse
#from django.template import Context

from tardis.tardis_portal.shortcuts import render_response_index
from MonashANDSService import MonashANDSService
from tardis.tardis_portal.models import Experiment

def index(request, experiment_id):
    url = 'monash_ands/form.html'
    e = Experiment.objects.get(id=experiment_id)

    if not request.POST:
        monashandsService = MonashANDSService(experiment_id)
        c = monashandsService.get_context(request)
        c['experiment'] = e
        return HttpResponse(render_response_index(request, url, c))
    else:
        monashandsService = MonashANDSService(experiment_id)
        c = monashandsService.register(request)
        c['experiment'] = e
        return HttpResponse(render_response_index(request, url, c))
