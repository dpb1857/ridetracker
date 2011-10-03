
from datetime import timedelta

class RiderTimeDelta(object):
    """
    Create a class like datetime.timedelta with some special properties.

    This timedelta has special time markers that represent a
    Did Not Finish or a Did Not Start, which are interpreted by the
    template format utility jinja2filters.py:format_ride_time() to dislay
    DNS or DNF rather than an actual time.
    """
    # XXX don't hardcode the checks in jinja2 filters, check for properties on this class;
    def __init__(self, start, end, dnf=False, dns=False):
        if dnf:
            days, seconds = (100, 0) # Marker for DNF;
        elif dns:
            days, seconds = (101, 0) # Marker for DNS;
        else:
            try:
                delta = end - start
                days, seconds = delta.days, delta.seconds
            except Exception:
                days, seconds = (102, 0) # Marker for Unknown;

        self.timedelta = timedelta(days=days, seconds=seconds)

    def __str__(self):
        
        return str(self.timedelta)

    def __unicode__(self):
        
        return str(self.timedelta)

    def __lt__(self, y):
        
        return self.timedelta.__lt__(y.timedelta)

    def __eq__(self, y):
        
        return self.timedelta.__eq__(y.timedelta)

    @property
    def days(self):
        
        return self.timedelta.days

    @property
    def seconds(self):

        return self.timedelta.seconds


# XXX pull in constants RIDE_START_TIME, RIDE_END_TIME from settings;
# in settings, do: import * from pbp2011.settings

from datetime import datetime

RIDE_START_TIME = datetime(2011, 8, 21, 16, 0)
RIDE_END_TIME = datetime(2011, 8, 25, 18, 0)


   
def constrain_ride_time(time):
    """
    Constrain the value of 'time' to be within [RIDE_START_TIME:RIDE_END_TIME], and 
    aligned it on a 15 minute boundary.
    """
    if time < RIDE_START_TIME:
        time = RIDE_START_TIME
    elif time > RIDE_END_TIME:
        time = RIDE_END_TIME

    if time.minute % 15 != 0 or time.second != 0:
        delta = timedelta(minutes=(time.minute%15), seconds=time.second)
        time = time - delta
        
    return time
