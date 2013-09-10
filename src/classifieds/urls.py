from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.edit import CreateView
from main.models.forms import UserCreationForms

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'inmo.views.home', name='home'),
    #  url(r'^inmo/', include('inmo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'', include(admin.site.urls)),

    url(r'^assets/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}
    ),

    url(r'^$', 'django.contrib.auth.views.login'),
	#url(r'^register$','main.views.registerUser'),
    url(r'^register', CreateView.as_view(
        template_name='register.html',
        form_class=UserCreationForms,
        success_url='/'
    )),
    url(r'^find/', 'main.views.viewClassified'),
    url(r'^create-ad/', 'main.views.addClassified'),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)
