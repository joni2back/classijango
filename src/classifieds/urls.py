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

    url(r'^$', 'main.views.index'),

    url(r'^api/json/location/cities', 'main.views.jsonCities'),

    url(r'^ads/find/', 'main.views.listClassifieds'),
    url(r'^ads/(?P<classifiedId>[0-9]{1,8})/(?P<classifiedTitle>[a-zA-Z0-9_\-\/]{0,95})$', 'main.views.viewClassified'),
    url(r'^ads/edit/(?P<classifiedId>[0-9]{1,8})$', 'main.views.editClassified'),
    url(r'^ads/delete/(?P<classifiedId>[0-9]{1,8})$', 'main.views.deleteClassified'),
    url(r'^ads/create/$', 'main.views.addClassified'),

    url(r'^accounts/register/$', 'main.views.registerUser'),
    url(r'^accounts/profile/$', 'main.views.myProfile'),
    url(r'^accounts/profile/classifieds$', 'main.views.myClassifieds'),
    url(r'^accounts/logout/$', 'main.views.logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'registration/password_change_form.html'}),
    url(r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'registration/password_change_done.html'}),

    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'), 
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    url(r'^admin/', include(admin.site.urls)),
)
