
from datetime import datetime, timedelta

from django.db import models
from django.contrib import admin

from django_countries import CountryField

# Create your models here.

RIDE_START_TIME = datetime(2011, 8, 21, 16, 0)
RIDE_END_TIME = datetime(2011, 8, 25, 18, 0)


class RiderTimeDelta(object):
    """
    Create a class like datetime.timedelta with some special properties.
    This timedelta has special time markers that represent a
    Did Not Finish or a Did Not Start, which are interpreted by the
    template format code in jinja2filters:format_ride_time() to dislay
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


def constrain_ride_time(time):

    if time < RIDE_START_TIME:
        time = RIDE_START_TIME
    elif time > RIDE_END_TIME:
        time = RIDE_END_TIME

    if time.minute % 15 != 0 or time.second != 0:
        delta = timedelta(minutes=(time.minute%15), seconds=time.second)
        time = time - delta
        
    return time


class BikeType(models.Model):
    bike_type = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.bike_type


class Control(models.Model):
    
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    distance = models.FloatField()

    def __unicode__(self):
        return "%d %s %05.1f" % (self.number, self.name, self.distance)

    @staticmethod
    def get_names():

        return [control.name for control in Control.objects.order_by('number')]

    @staticmethod
    def get_controls():

        return list(Control.objects.order_by('number'))

    @staticmethod
    def get_num_controls():

        return len(Control.objects.all())


class Checkpoint(models.Model):
    
    checkpoint_number = models.IntegerField()
    frame_number = models.IntegerField(db_index=True)
    time = models.DateTimeField(db_index=True)

class Rider(models.Model):
    frame_number = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    country = CountryField()
    bike_type = models.ForeignKey(BikeType)

    dnf = models.BooleanField(default=False) 
    dns = models.BooleanField(default=False) 

    def __unicode__(self):
        return "%d %s %s" % (self.frame_number, self.first_name, self.last_name)

    @property
    def checkpoint_times(self):
        checkpoints = Checkpoint.objects.filter(frame_number=self.frame_number)
        values = Control.get_num_controls() * [None]
        for cp in checkpoints:
            values[cp.checkpoint_number-1] = cp.time
        return values

    @property
    def elapsed(self):
        times = self.checkpoint_times
        return RiderTimeDelta(times[0], times[14], dns=self.dns, dnf=self.dnf)

    # XXX would it make more sense for this just be a property on a Rider object rather than a staticmethod?

    @staticmethod
    def get_locations(frame_num):
        """
        Return a list containing the rider position at each timeslice during
        the ride.
        """
        controls = Control.get_controls()
        control_times = [None] * len(controls)
        for checkpoint in Checkpoint.objects.filter(frame_number=frame_num):
            control_times[checkpoint.checkpoint_number-1] = checkpoint.time

        while control_times and control_times[-1] is None:
            del control_times[-1]

        locations = []
        current_time = RIDE_START_TIME
        while current_time <= RIDE_END_TIME:
            locations.append(int(Rider.get_location(current_time, controls, control_times)))
            current_time += timedelta(minutes=15)

        return locations

    @staticmethod
    def get_location(when, controls, times):
        """
        Return the rider location at WHEN.
        controls is a list of control objects,
        times is the list of checkpoint times for the rider.
        """
        # Start control only - no data for positioning;
        if len(times) == 1:
            return controls[-1].distance

        # Rider hasn't started yet;
        if when <= times[0]:
            return controls[0].distance

        # Past the final time for this rider;
        if when >= times[-1]:
            return controls[-1].distance

        min = 0
        max = len(times) -1
        while min+1 < max:
            median = (min+max)/2
            if when < times[median]:
                max = median
            else:
                min = median

        # ASSERT: times[min] <= when < times[max]

        speed = (controls[max].distance-controls[min].distance)/(times[max]-times[min]).total_seconds()
        extra_distance = speed * (when - times[min]).total_seconds()
        return controls[min].distance + extra_distance
