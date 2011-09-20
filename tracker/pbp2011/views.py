
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.cache import cache_page
from django.views.generic.simple import redirect_to

from django_countries import countries

from jinja2 import FileSystemLoader, Environment

import models
import jinja2filters

template_dirs = getattr(settings, 'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = Environment(loader=FileSystemLoader(template_dirs))
env.filters['url'] = jinja2filters.url
env.filters['format_ride_time'] = jinja2filters.format_ride_time

countries.OFFICIAL_COUNTRIES['TW'] = countries.OFFICIAL_COUNTRIES['TW'].split(',')[0]

# Create your views here.

DISABLE_CACHE = False

if DISABLE_CACHE:
    def cache_page(*args, **kwargs):
        def noop_decorator(func):
            return func
        return noop_decorator

def raise_exception(request):
    """
    Verify that your installed configuration handles system exceptions the way you want it to -
    check that email gets sent, proper exception page show to user, etc.
    """
    raise Exception("Let's test error handling")


@cache_page(86400 * 7)
def country(request):

    class Results(object):

        def __init__(self, cc):
            self.cc = cc
            self.registered = 0
            self.dns = 0
            self.dnf = 0
        
        def add_rider(self, rider):
            self.registered += 1

            if rider.dns:
                self.dns += 1

            if rider.dnf:
                self.dnf += 1

        def finish_rate(self):
            
            rate = 100*(self.registered-self.dns-self.dnf)/(self.registered-self.dns)
            return rate

    results = {}
    for rider in models.Rider.objects.all():
        cc = rider.country.code
        results[cc] = results.get(cc, Results(cc))
        results[cc].add_rider(rider)

    results = results.values()
    sort = request.GET.get('sort', 'country')

    if sort == "country":
        results.sort(key=lambda x: x.cc)
    elif sort == "registered":
        results.sort(key=lambda x: x.registered, reverse=True)
    elif sort == "rate":
        results.sort(key=lambda x: x.registered, reverse=True)
        results.sort(key=lambda x: x.finish_rate(), reverse=True)

    total_registered = sum([r.registered for r in results])
    total_dns = sum([r.dns for r in results])
    total_dnf = sum([r.dnf for r in results])
    overall_finish_rate = 100 * (total_registered-total_dns-total_dnf)/(total_registered-total_dns)

    template = env.get_template("country.html")
    rendered = template.render(dict(results=results,
                                    country_names=countries.OFFICIAL_COUNTRIES,
                                    registered=total_registered,
                                    total_dns=total_dns,
                                    total_dnf=total_dnf,
                                    overall_finish_rate=overall_finish_rate,
                                    ))

    return HttpResponse(rendered)
    
@cache_page(86400 * 7)
def riders(request, country_code=None, template_name=None):

    country_name = ""
    if country_code:
        country_code = country_code.upper()
        if country_code == "UK":
            return redirect_to(request, reverse('pbp2011.views.riders', args=("GB",)), query_string=True)

        country_name = countries.OFFICIAL_COUNTRIES.get(country_code, None)
        if not country_name:
            return respond(request, template_name="error-message.html", message="Unrecognized country code: %s" % country_code, response=HttpResponseNotFound)

    show_country = True if country_code is None else False

    riders = models.Rider.objects.all()
    if country_code:
        riders = riders.filter(country=country_code)

    riders = list(riders)
    sort = request.GET.get('sort', 'frame')
    
    if sort == "frame":
        riders.sort(key=lambda x: x.frame_number)
    elif sort == "name":
        riders.sort(key=lambda x: x.first_name)
        riders.sort(key=lambda x: x.last_name)
    elif sort == "time":
        riders.sort(key=lambda x: x.first_name)
        riders.sort(key=lambda x: x.last_name)
        riders.sort(key=lambda x: x.elapsed)

    template = env.get_template(template_name)
    rendered = template.render(dict(riders=riders, country=country_name, show_country=show_country))

    return HttpResponse(rendered)

def frame(request, frame_number):

    rider = models.Rider.objects.get(frame_number=frame_number)
    times = rider.checkpoint_times
    elapsed_times = [models.RiderTimeDelta(times[0], t) for t in times]

    template = env.get_template("frame.html")
    rendered = template.render(dict(rider=rider,
                                    control_names=models.Control.get_names(),
                                    times=times,
                                    elapsed_times=elapsed_times
                                    ))

    return HttpResponse(rendered)

def respond(request, template_name=None, response=HttpResponse, **kwargs):
    
    template = env.get_template(template_name)
    rendered = template.render(**kwargs)
    return response(rendered)

def histogram(request):

    template = env.get_template("histogram.html")
    rendered = template.render()
    return HttpResponse(rendered)
