# -*- coding: utf-8 -*-

from django.template import Context
from django.shortcuts import render_to_response

from tardis.tardis_portal.views import getNewSearchDatafileSelectionForm


from tardis.apps.equipment.forms import EquipmentSearchForm
from tardis.apps.equipment.models import Equipment


def view_equipment(request, object_key):

    q = Equipment.objects.get(key__iexact=object_key)
    c = Context({'object': q,
                 'searchDatafileSelectionForm':
                     getNewSearchDatafileSelectionForm()})
    return render_to_response('equipment/equipment_detail.html', c)


def search_equipment(request):
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

            c = Context({'object_list': q })
            return render_to_response('equipment/equipment_list.html', c)
    else:
        form = EquipmentSearchForm()

    c = Context({'form': form })
    return render_to_response('equipment/search_equipment.html', c)
