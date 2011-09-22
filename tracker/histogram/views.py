
import pickle
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from django.views.decorators.cache import cache_page

import models

# Create your views here.

def compute_histogram(request):

    models.compute_pbp2011_histogram()
    return HttpResponse("Done.")

@cache_page(60*60)
def hist_data(request, datespec):

    try:
        time = datetime.strptime(datespec, "%Y-%m-%d %H:%M")
    except:
        return HttpResponseBadRequest("400 Bad Request: Could not parse datespec.")

    if time < models.PBP2011_START_TIME:
        time = models.PBP2011_START_TIME
    elif time > models.PBP2011_END_TIME:
        time = models.PBP2011_END_TIME

    if time.minute % 15 != 0 or time.second != 0:
        delta = timedelta(minutes=(time.minute%15), seconds=time.second)
        time = time - delta

    try:
        location = models.Location.objects.get(time=time)
        locations = pickle.loads(str(location.histogram))
    except:
        return HttpResponseNotFound("404 Not Found: Could not find record for datespec %s" % datespec)

    return HttpResponse(simplejson.dumps(dict(data=locations)), mimetype="application/json")

