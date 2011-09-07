from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# uncommented by django_bootstrap.py
from django.contrib import admin
# uncommented by django_bootstrap.py
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),

    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'pbp2011/', 'permanent': True}),
    url(r'^pbp2011/', include('tracker.pbp2011.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # uncommented by django_bootstrap.py
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # uncommented by django_bootstrap.py
    url(r'^admin/', include(admin.site.urls)),
)
