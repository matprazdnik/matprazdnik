from django.conf.urls import patterns, include, url
from matprazdnik import settings

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

    url(r'^flying_rows/', include('flying_rows.urls')),

    url(r'^$', 'main_app.views.participants'),

    url(r'^participants/$', 'main_app.views.participants'),
    url(r'^schools/$', 'main_app.views.schools'),
    url(r'^points/$', 'main_app.views.points'),
    url(r'^diplomas/$', 'main_app.views.diplomas'),
    url(r'^diplomas_csv/$', 'main_app.views.diplomas_csv'),
    url(r'^stats/$', 'main_app.views.stats'),
    url(r'^missing/$', 'main_app.views.missing'),
    url(r'^final_check/$', 'main_app.views.final_check'),
    # url(r'^update_participants/$', 'main_app.views.update_participants'),
    # TODO: what is it?

    url(r'^new/workcode_form$', 'main_app.views.workcode_form'),
    url(r'^new/score_form$', 'main_app.views.score_form'),
)

if settings.DEBUG is False:   # if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
