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
    url(r'^feeder/add/$', feeder.add_feeder, name='feeder-add'),
    url(r'^location/add/$', feeder.add_location, name='location-add'),
    url(r'^feeder-type/$', feeder.list_feeder_type, name='feeder-type-list'),
    url(r'^feeder-type/add/$', feeder.edit_feeder_type, name='feeder-type-add'),
    url(r'^feeder-type/edit/(?P<id>\d+)/$', feeder.edit_feeder_type, name='feeder-type-edit'),
    url(r'^status/add/$', feeder.add_status, name='status-add'),
)
