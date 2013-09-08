from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'inmo.views.home', name='home'),
    #  url(r'^inmo/', include('inmo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'', include(admin.site.urls)),
    #url(r'^receta/(?P<id_receta>\d+)$','principal.views.detalle_receta'),
	url(r'^register$','main.views.registerUser'),
	#url(r'^usuarios/$','principal.views.usuarios'),
    url(r'^classified/', 'main.views.viewClassified'),
    url(r'^addclassified/', 'main.views.addClassified'),
    url(r'^admin/', include(admin.site.urls)),
)
