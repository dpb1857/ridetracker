
import pickle
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils import simplejson
from django.views.decorators.cache import cache_page

import models
import pbp2011.models as ridemodels

from tracker import util

# Create your views here.

DISABLE_CACHE = getattr(settings, 'DISABLE_CACHE', False)

if DISABLE_CACHE:
    def cache_page(*args, **kwargs):
        def noop_decorator(func):
            return func
        return noop_decorator

def compute_histogram(request):

    models.compute_pbp2011_histogram()
    return HttpResponse("Done.")

@cache_page(60*60)
def hist_data(request, datespec):
    """
    """
    try:
        time = datetime.strptime(datespec, "%Y-%m-%d %H:%M")
    except:
        return HttpResponseBadRequest("400 Bad Request: Could not parse datespec.")

    time = util.constrain_ride_time(time)

    try:
        location = models.Location.objects.get(time=time)
        locations = pickle.loads(str(location.histogram))
    except:
        return HttpResponseNotFound("404 Not Found: Could not find record for datespec %s" % datespec)

    # XXX call function in models to compute time index;
    time_index = int((time-ridemodels.RIDE_START_TIME).total_seconds())/(60*15)
    result = {
        'data': locations,
        'time_index': time_index # models.time_to_time_index(time)
        }

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@cache_page(60*60)
def frame_data(request, frame_num):

    try:
        rider = ridemodels.Rider.objects.get(frame_number=frame_num)
    except:
        return HttpResponseNotFound("404 Not Found: Could not find frame number %s" % frame_num)

    result_dict = {
        'framenum': frame_num,
        'data': rider.get_locations(),
        'name': ' '.join((rider.first_name,rider.last_name)),
        }
    
    return HttpResponse(simplejson.dumps(result_dict), mimetype="application/json")
