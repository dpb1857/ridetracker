
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'country', 'permanent': True}),

    (r'^riders$', 'pbp2011.views.riders', {'template_name': 'riders_all.html'}),
    (r'^country/?$', 'pbp2011.views.country'),
    (r'^country/(\w+)$', 'pbp2011.views.riders', {'template_name': 'riders_country.html'}),
    (r'^frame/(\d+)$', 'pbp2011.views.frame'),
    (r'^histogram$', 'pbp2011.views.histogram'),

    (r'^raise_exception$', 'pbp2011.views.raise_exception'),
#   (r'^admin/import_data$', 'pbp2011.views.import_data'),
                       
    (r'^help/?$', 'django.views.generic.simple.redirect_to', {'url': 'help/about', 'permanent': True}, "pbp2011-help"),
    (r'^help/about$', 'pbp2011.views.respond', {'template_name': 'help-about.html'}, "pbp2011-help-about"),
    (r'^help/related$', 'pbp2011.views.respond', {'template_name': 'help-related.html'}, "pbp2011-help-related"),
)
