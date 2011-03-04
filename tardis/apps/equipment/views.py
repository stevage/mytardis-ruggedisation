# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context

from tardis.tardis_portal.shortcuts import render_response_index
from tardis.tardis_portal.views import getNewSearchDatafileSelectionForm

from tardis.apps.equipment.forms import EquipmentSearchForm
from tardis.apps.equipment.models import Equipment


def index(request):

    c = Context({'object_list': Equipment.objects.all(),
                 'paginate_by': 15,
                 'searchDatafileSelectionForm':
                     getNewSearchDatafileSelectionForm()})
    url = 'equipment/equipment_list.html'
    return HttpResponse(render_response_index(request, url, c))


def view(request, object_id):

    c = Context({'object': Equipment.objects.get(pk=object_id),
                 'searchDatafileSelectionForm':
                     getNewSearchDatafileSelectionForm()})
    url = 'equipment/equipment_detail.html'
    return HttpResponse(render_response_index(request, url, c))


def search(request):
    if request.method == 'POST':
        form = EquipmentSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            q = Equipment.objects.all()
            if data['key']:
                q = q.filter(key__icontains=data['key'])
            if data['description']:
                q = q.filter(description__icontains=data['description'])
            if data['make']:
                q = q.filter(make__icontains=data['make'])
            if data['serial']:
                q = q.filter(serial__icontains=data['serial'])
            if data['type']:
                q = q.filter(type__icontains=data['type'])

            c = Context({'header': 'Search Equipment',
                         'object_list': q,
                         'searchDatafileSelectionForm':
                             getNewSearchDatafileSelectionForm()})
            url = 'equipment/equipment_list.html'
            return HttpResponse(render_response_index(request, url, c))
    else:
        form = EquipmentSearchForm()

    c = Context({'form': form,
                 'searchDatafileSelectionForm':
                     getNewSearchDatafileSelectionForm()})
    url = 'equipment/equipment_search.html'
    return HttpResponse(render_response_index(request, url, c))