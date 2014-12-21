from django.conf.urls import patterns, include, url

from django.contrib import admin
from camfeeder.feeder import views as feeder
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    
    # Django default login
    url(r'^accounts/logout/$','django.contrib.auth.views.logout', name='account-logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='account-login'),
    
    url(r'^$', feeder.list_, name='feeder-list'),
    url(r'^dashboard/$', feeder.feeder_dashboard, name='feeder-dashboard'),
    url(r'^feeder/add/$', feeder.add_or_edit_feeder, name='feeder-add'),
    url(r'^feeder/edit/(?P<id>\d+)/$', feeder.add_or_edit_feeder, name='feeder-edit'),
    url(r'^location/$', feeder.list_location, name='location-list'),
    url(r'^location/add/$', feeder.add_or_edit_location, name='location-add'),
    url(r'^location/edit/(?P<id>\d+)/$', feeder.add_or_edit_location, name='location-edit'),
    url(r'^feeder-type/$', feeder.list_feeder_type, name='feeder-type-list'),
    url(r'^feeder-type/add/$', feeder.add_or_edit_feeder_type, name='feeder-type-add'),
    url(r'^feeder-type/edit/(?P<id>\d+)/$', feeder.add_or_edit_feeder_type, name='feeder-type-edit'),
    url(r'^symptom/$', feeder.list_symptom, name='symptom-list'),
    url(r'^symptom/add/$', feeder.add_or_edit_symptom, name='symptom-add'),
    url(r'^symptom/edit/(?P<id>\d+)/$', feeder.add_or_edit_symptom, name='symptom-edit'),
    url(r'^actiontaken/$', feeder.list_actiontaken, name='actiontaken-list'),
    url(r'^actiontaken/add/$', feeder.add_or_edit_actiontaken, name='actiontaken-add'),
    url(r'^actiontaken/edit/(?P<id>\d+)/$', feeder.add_or_edit_actiontaken, name='actiontaken-edit'),
    url(r'^top_symptom_json/$',feeder.top_symptom_json, name='top_symptom_json'),
    url(r'^top_symptom_json_by_feeder/(?P<feeder_id>\d+)/$',feeder.top_symptom_json_by_feeder, name='top_symptom_json_by_feeder'),
    url(r'^filter/$', feeder.top_symptom_json_by_location_by_feeder_type, name='filter_url'),
)
