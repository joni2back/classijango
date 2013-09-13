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
    url(r'^accounts/profile/$', 'main.views.index'),
    
    #url(r'^register', CreateView.as_view(
    #    template_name='register.html',
    #    form_class=UserCreationForms,
    #    success_url='/'
    #)),
    
    url(r'^account/register/$', 'main.views.registerUser'),
    url(r'^find/', 'main.views.viewClassified'),
    url(r'^create-ad/', 'main.views.addClassified'),
    url(r'^account/logout/', 'main.views.logout'),
    url(r'^account/login/', 'django.contrib.auth.views.login'),
    #url(r'^login/', 'main.views.loginUser'),
    url(r'^admin/', include(admin.site.urls)),
)
