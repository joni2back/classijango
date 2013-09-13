# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.edit import CreateView
from main.forms import *
from django.conf.urls import *

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^assets/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}
    ),

    url(r'^$', 'main.views.index'),
   
    
    url(r'^find/', 'main.views.viewClassified'),
    url(r'^create-ad/', 'main.views.addClassified'),
    
    url(r'^accounts/register/$', 'main.views.registerUser'),
    url(r'^accounts/profile/', 'main.views.myProfile'),
    url(r'^accounts/logout/', 'main.views.logout'),
    url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    
    url(r'^admin/', include(admin.site.urls)),
)
