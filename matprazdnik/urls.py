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

    url(r'^$', 'main_app.views.participants'),
    url(r'^participants/update/$', 'main_app.views.update_participants'),
    url(r'^participants/add/$', 'main_app.views.add_participants'),
    url(r'^participants/getnew/$', 'main_app.views.get_new'),
    url(r'^participants/$', 'main_app.views.participants'),
    url(r'^schools/$', 'main_app.views.schools'),
    url(r'^points/$', 'main_app.views.points'),
    url(r'^diplomas/$', 'main_app.views.diplomas'),
)
