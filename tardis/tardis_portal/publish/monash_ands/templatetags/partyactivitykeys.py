'''
Party / Activity parameter retreival template tags.
To be used with the Monash ANDS Publish Provider PublishProvider

.. moduleauthor:: Steve Androulakis <steve.androulakis@monash.edu>
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import template

from tardis.tardis_portal.models import ExperimentParameter

register = template.Library()


@register.filter
def party_keys(value):
    """
    Return associated Research Master Party Keys for given experiment

    :param value: The experiment_id
    :type string:

    """
    result = ExperimentParameter.objects.filter(name__name='party_id',
    parameterset__schema__namespace='http://localhost/pilot/party/1.0/',
    parameterset__experiment__id=value)

    return result


@register.filter
def activity_keys(value):
    """
    Return associated Research Master Activity Keys for given experiment

    :param value: The experiment_id
    :type string:

    """
    result = ExperimentParameter.objects.filter(name__name='activity_id',
    parameterset__schema__namespace='http://localhost/pilot/activity/1.0/',
    parameterset__experiment__id=value)

    return result
