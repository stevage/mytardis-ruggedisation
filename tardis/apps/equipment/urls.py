from django.conf.urls.defaults import patterns
from django.views.generic import list_detail

from tardis.apps.equipment.models import Equipment


urlpatterns = patterns('',
                       (r'^$', list_detail.object_list,
                        {'queryset': Equipment.objects.all(),
                         'paginate_by': 15,
                         'extra_context': {}}),
                       (r'^search/$',
                        'tardis.apps.equipment.views.search_equipment'),
                       (r'^(?P<object_id>\d+)/$', list_detail.object_detail,
                        {'queryset': Equipment.objects.all()}),
                       (r'^(?P<object_key>\w+)/$',
                        'tardis.apps.equipment.views.view_equipment'),
                       )
