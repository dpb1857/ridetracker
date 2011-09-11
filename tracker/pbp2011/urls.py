
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'country', 'permanent': True}),
    (r'^riders$', 'pbp2011.views.riders', {'template_name': 'riders_all.html'}),
    (r'^country/?$', 'pbp2011.views.country'),
    (r'^country/(\w{2})$', 'pbp2011.views.riders', {'template_name': 'riders_country.html'}),
    (r'^frame/(\d+)$', 'pbp2011.views.frame'),

#   (r'^admin/import_data$', 'pbp2011.views.import_data'),
)
