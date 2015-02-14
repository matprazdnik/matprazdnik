from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^load_new_rows/$', 'flying_rows.views.load_new_rows'),
    url(r'^add_new_row/$', 'flying_rows.views.add_new_row'),
    url(r'^update_field/$', 'flying_rows.views.update_field'),
    url(r'^autocomplete/$', 'flying_rows.views.load_autocomplete_choices'),
    url(r'^search/$', 'flying_rows.views.search'),
    url(r'^search_hints/$', 'flying_rows.views.get_search_hints'),
)
