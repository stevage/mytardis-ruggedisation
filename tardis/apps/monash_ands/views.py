# -*- coding: utf-8 -*-

from django.http import HttpResponse
#from django.template import Context

from tardis.tardis_portal.shortcuts import render_response_index
from MonashANDSService import MonashANDSService
from tardis.tardis_portal.models import Experiment
from tardis.apps.monash_ands.ldap_query import \
    LDAPUserQuery
from django.contrib.auth.decorators import login_required
from tardis.tardis_portal.creativecommonshandler import CreativeCommonsHandler

def index(request, experiment_id):
    url = 'monash_ands/form.html'
    e = Experiment.objects.get(id=experiment_id)

    if not request.POST:
        monashandsService = MonashANDSService(experiment_id)
        c = monashandsService.get_context(request)
        c['experiment'] = e

        cch = CreativeCommonsHandler(experiment_id=experiment_id)
        c['has_cc_license'] = cch.has_cc_license()

        return HttpResponse(render_response_index(request, url, c))
    else:
        monashandsService = MonashANDSService(experiment_id)
        c = monashandsService.register(request)
        c['experiment'] = e

        return HttpResponse(render_response_index(request, url, c))

@login_required()
def retrieve_ldap_user_list(request):

    if 'q' in request.GET:
        if len(request.GET['q']) < 3:
            return HttpResponse('')
        else:
            query_input = request.GET['q']
            l = LDAPUserQuery()

            userlist = '\n'.join([LDAPUserQuery.get_user_attr(u, 'mail') for u in \
                l.get_users(query_input)])

        return HttpResponse(userlist)
    else:
        return HttpResponse('')
