# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

from tardis.tardis_portal.models import *

register = template.Library()


@register.filter
def eparametertypecheck(value, arg):
    experimentparameter = ExperimentParameter.objects.get(id=arg)

    if experimentparameter.name.units.startswith('image'):
        result = "<img src='/display/ExperimentImage/load/%i/'" % arg
        return mark_safe(result)
    elif experimentparameter.name.name.endswith('Image'):
        eid = experimentparameter.parameterset.experiment.id
        psid = experimentparameter.parameterset.id
        result = "<img src='/display/ExperimentImage/%s/%s/%s/'" \
            % (eid, psid, experimentparameter.name.name)
        return mark_safe(result)
    else:
        return value


@register.filter
def dsparametertypecheck(value, arg):
    datasetparameter = DatasetParameter.objects.get(id=arg)

    if datasetparameter.name.units.startswith('image'):
        result = "<img src='/display/DatasetImage/load/%i/'" % arg
        return mark_safe(result)
    elif datasetparameter.name.name.endswith('Image'):
        dsid = datasetparameter.parameterset.dataset.id
        psid = datasetparameter.parameterset.id
        result = "<img src='/display/DatasetImage/%s/%s/%s/'" \
            % (dsid, psid, datasetparameter.name.name)
        return mark_safe(result)
    else:
        return value


@register.filter
def dfparametertypecheck(value, arg):
    datafileparameter = DatafileParameter.objects.get(id=arg)

    if datafileparameter.name.units.startswith('image'):
        result = "<img src='/display/DatafileImage/load/%i/'" % arg
        return mark_safe(result)
    elif datafileparameter.name.name.endswith('Image'):
        dfid = datafileparameter.parameterset.dataset_file.id
        psid = datafileparameter.parameterset.id
        result = "<img src='/display/DatafileImage/%s/%s/%s/'" \
            % (dfid, psid, datafileparameter.name.name)
        return mark_safe(result)
    else:
        return value
