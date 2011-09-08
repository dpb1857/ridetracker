
import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from django_countries import countries

from jinja2 import FileSystemLoader, Environment

import models
import jinja2filters

template_dirs = getattr(settings, 'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = Environment(loader=FileSystemLoader(template_dirs))
env.filters['url'] = jinja2filters.url

tw = countries.OFFICIAL_COUNTRIES['TW'] = countries.OFFICIAL_COUNTRIES['TW'].split(',')[0]

def format_elapsed(delta):

    if not delta:
        return ""

    hours = delta.days*24 + delta.seconds/3600
    mins = (delta.seconds % 3600)/60
    return "%02d:%02d" % (hours, mins)



# Create your views here.

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
    
# return HttpResponse("list of countries:<br>" + '<br> '.join(countries))

def country_detail(request, country_code):

    def rider_status(rider):

        if rider.dns: 
            return "DNS"
        elif rider.dnf:
            return "DNF"
        else:
            try:
                return format_elapsed(rider.cp15-rider.cp1)
            except Exception:
                return "Unknown"

    country_code = country_code.upper()
    riders = list(models.Rider.objects.filter(country=country_code))

    sort = request.GET.get('sort', 'frame')
    
    if sort == "frame":
        riders.sort(key=lambda x: x.frame_number)
    elif sort == "name":
        riders.sort(key=lambda x: x.first_name)
        riders.sort(key=lambda x: x.last_name)
    elif sort == "time":
        riders.sort(key=lambda x: x.first_name)
        riders.sort(key=lambda x: x.last_name)
        riders.sort(key=lambda x: rider_status(x))

    template = env.get_template("country_detail.html")
    rendered = template.render(dict(riders=riders,
                                    country=countries.OFFICIAL_COUNTRIES[country_code],
                                    status=rider_status
                                    ))

    return HttpResponse(rendered)

def frame(request, frame_number):

    CONTROL_NAMES = [
        "SQY",
        "Villaines",
        "Fougeres",
        "Tinteniac",
        "Loudeac",
        "Carhaix",
        "Brest",
        "Carhaix",
        "Loudeac",
        "Tinteniac",
        "Fougeres",
        "Villaines",
        "Mortagne",
        "Dreux",
        "SQY"
        ]

    rider = models.Rider.objects.get(frame_number=frame_number)
    times = [getattr(rider, "cp%d"%i) for i in range(1, 16)]
    elapsed = [t-times[0] if t else None for t in times]

    times = [t.strftime("%m/%d %H:%M") if t else "" for t in times]
    elapsed = [format_elapsed(e) for e in elapsed]

    time_tuples = zip(CONTROL_NAMES, times, elapsed)

    template = env.get_template("frame.html")
    rendered = template.render(dict(rider=rider,
                                    times=time_tuples,
                                    ))

    return HttpResponse(rendered)

    
