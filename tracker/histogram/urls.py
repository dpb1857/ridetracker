
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',

    (r'^compute_histogram', 'histogram.views.compute_histogram'),
    (r'^histdata/full$', 'histogram.views.full_hist_data'),
    (r'^histdata/([\w: -]+)$', 'histogram.views.hist_data'),
    (r'^framedata/(\d+)$', 'histogram.views.frame_data'),
)
