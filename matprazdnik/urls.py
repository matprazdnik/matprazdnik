from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'matprazdnik.views.home', name='home'),
    # url(r'^matprazdnik/', include('matprazdnik.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^participants/', 'main_app.views.participants'),
    url(r'^schools/', 'main_app.views.schools'),
    url(r'^registration/', 'main_app.views.registration'),
    url(r'^points/', 'main_app.views.points'),
    url(r'^diplomas/', 'main_app.views.diplomas'),
)
