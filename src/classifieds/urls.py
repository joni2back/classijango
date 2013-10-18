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
    url(r'^uploads/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT}
    ),

    url(r'^api/json/location/cities', 'main.views.jsonCities'),

    url(r'^$', 'main.views.index'),    
    url(r'^ads/find/', 'main.views.listClassifieds'),
    url(r'^ads/(?P<classifiedTitle>[a-zA-Z0-9_\-]{0,64}):(?P<classifiedId>[0-9]{1,8})$', 'main.views.viewClassified'),
    url(r'^ads/edit/(?P<classifiedId>[0-9]{1,8})$', 'main.views.editClassified'),
    url(r'^ads/delete/(?P<classifiedId>[0-9]{1,8})$', 'main.views.deleteClassified'),
    url(r'^ads/create/$', 'main.views.addClassified'),
    url(r'^accounts/register/$', 'main.views.registerUser'),
    url(r'^accounts/profile/$', 'main.views.myProfile'),
    url(r'^accounts/profile/classifieds$', 'main.views.myClassifieds'),
    url(r'^accounts/logout/$', 'main.views.logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)
