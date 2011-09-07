
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'country', 'permanent': True}),
    (r'^country/?$', 'pbp2011.views.country'),
    (r'^country/(\w{2})$', 'pbp2011.views.country_detail'),
    (r'^frame/(\d+)$', 'pbp2011.views.frame'),
)

