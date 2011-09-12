
# Downloaded from http://djangosnippets.org/snippets/1062/

from django.template.defaulttags import URLNode
from django.conf import settings
from jinja2.filters import contextfilter
from django.utils import translation



def url(view_name, *args, **kwargs):
    from django.core.urlresolvers import reverse, NoReverseMatch
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        try:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            return reverse(project_name + '.' + view_name,
                           args=args, kwargs=kwargs)
        except NoReverseMatch:
            return ''

def nbspize(text):
    import re
    return re.sub('\s','&nbsp;',text.strip())

def get_lang():
    return translation.get_language()

def timesince(date):
    from django.utils.timesince import timesince
    return timesince(date)

def timeuntil(date):
    from django.utils.timesince import timesince
    from datetime import datetime
    return timesince(datetime.now(),datetime(date.year, date.month, date.day))

def truncate(text,arg):
    import re
    from django.utils.encoding import force_unicode
    text = force_unicode(text)
    matches = re.match('(\d+)([cw]{1})',arg)
    if not matches:
        return text
    count = int(matches.group(1))
    type = matches.group(2)

    if type == 'c':
        if count > len(text):
            return text
        else:
            return text[:count] + '&hellip;'
    elif type == 'w':
        arr = text.strip().split()
        if count > len(arr):
            return ' '.join(arr)
        else:
            return ' '.join(arr[:count]) + '&hellip;'

# Added by dpb

def _check_sentinel(delta):
        
    if delta.days == 100:
        return "DNF"
    if delta.days == 101:
        return "DNS"
    if delta.days == 102:
        return "Unknown"

    return None

def format_ride_time(delta, show_special=True):

    special = _check_sentinel(delta)
    if special:
        if show_special:
            return special
        else:
            return ""

    hours = delta.days*24 + delta.seconds/3600
    mins = (delta.seconds % 3600)/60
    return "%d:%02d" % (hours, mins)

