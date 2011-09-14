
from datetime import timedelta

from django.db import models
from django.contrib import admin

from django_countries import CountryField

# Create your models here.

class RiderTimeDelta(object):
    
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

        return len(Control.get_names())


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

