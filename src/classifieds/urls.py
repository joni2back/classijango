# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.edit import CreateView
from main.models.forms import UserRegistrationForm
from django.conf.urls.defaults import *

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    #url(r'', include(admin.site.urls)),

    url(r'^assets/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}
    ),

    url(r'^$', 'django.contrib.auth.views.login'),
    #url(r'^register', CreateView.as_view(
    #    template_name='register.html',
    #    form_class=UserCreationForms,
    #    success_url='/'
    #)),
    
    url(r'^register/$', 'main.views.registerUser'),
    url(r'^find/', 'main.views.viewClassified'),
    url(r'^create-ad/', 'main.views.addClassified'),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)
