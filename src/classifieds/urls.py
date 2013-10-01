# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.edit import CreateView
from main.forms import *
from django.conf.urls import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^assets/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT}
    ),

    url(r'^api/json/location/cities', 'main.views.jsonCities'),
    #url(r'^api/json/location/cities/(?P<provinceId>[0-9]{0,3})$', 'main.views.jsonCities'),
    #url(r'^api/json/location/provinces/(?P<countryId>[0-9]{0,3})$', 'main.views.jsonProvinces'),
    #url(r'^api/json/location/countries/$', 'main.views.jsonCountries'),

    url(r'^$', 'main.views.index'),    
    url(r'^ads/find/', 'main.views.listClassifieds'),
    url(r'^ads/(?P<classifiedTitle>[a-zA-Z_-]{0,64})-(?P<classifiedId>[0-9]{1,6})$', 'main.views.viewClassified'),
    url(r'^ads/create/$', 'main.views.addClassified'),
    url(r'^accounts/register/$', 'main.views.registerUser'),
    url(r'^accounts/profile/$', 'main.views.myProfile'),
    url(r'^accounts/logout/$', 'main.views.logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)
