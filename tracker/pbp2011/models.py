# disable line length;
#pylint: disable=C0301


from datetime import datetime, timedelta

from django.db import models
from django.contrib import admin

from django_countries import CountryField

from tracker.util import RiderTimeDelta

# Create your models here.

RIDE_START_TIME = datetime(2011, 8, 21, 16, 0)
RIDE_END_TIME = datetime(2011, 8, 25, 18, 0)

############################################################
# Models correspond to migration 0003
############################################################

# XXX let's get rid of this, make it part of the rider model;

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
    def control_at(distance):
        
        if not hasattr(Control, "_control_distances"):
            ctl_dict = {}
            for c in Control.objects.all():
                ctl_dict[int(c.distance)] = c
            Control._control_distances = ctl_dict

        return Control._control_distances.get(distance, "")

    @staticmethod
    def get_controls():

        return list(Control.objects.order_by('number'))

    @staticmethod
    def get_num_controls():

        return len(Control.objects.all())


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

    def __repr__(self):
       return "Rider(%d, %s %s)" % (self.frame_number, self.first_name, self.last_name)

    @property
    def waypoints(self):
        """
        This property is a list of all waypoints for a rider.
        """
        if not hasattr(self, "_waypoints"):
            waypoints = list(Waypoint.objects.filter(frame_key=self.frame_number).order_by('timestamp'))
            if waypoints:
                new_waypoints = [waypoints[0]]
                waypoints = waypoints[1:]
                while waypoints:
                    prev_waypoint = new_waypoints[-1]
                    next_waypoint = waypoints[0]
                    if next_waypoint.transition == Waypoint.TRANSITION_ARRIVAL:
                        # Generate a fake departure waypoint;
                        syn_waypoint = Waypoint()
                        syn_waypoint.frame_key = prev_waypoint.frame_key
                        syn_waypoint.kilometers = prev_waypoint.kilometers
                        syn_waypoint.transition = Waypoint.TRANSITION_DEPARTURE
                        syn_waypoint.timestamp = prev_waypoint.timestamp + timedelta(hours=1)
                        syn_waypoint.data_source = Waypoint.SOURCE_SYNTHETIC
                        new_waypoints.append(syn_waypoint)

                    new_waypoints.append(next_waypoint)
                    waypoints = waypoints[1:]

                waypoints = new_waypoints

            self._waypoints = waypoints

        return self._waypoints

    @property
    def elapsed(self):
        """
        Take the delta-t between the last and first controls.
        """
	if not self.dns:
	    waypoints = self.waypoints

	if self.dns or not waypoints:
	    return RiderTimeDelta(None, None, dns=self.dns, dnf=self.dnf)
        else:
	    return RiderTimeDelta(waypoints[0].timestamp, waypoints[-1].timestamp, dns=self.dns, dnf=self.dnf)

    # XXX would it make more sense for this just be a property on a Rider object rather than a method?

    # XXX Add RideMeta with event start, event end, time_quanta;

    def get_locations(self):
        """
        Return a list containing the rider position at each timeslice during
        the ride. The value is an integer to represent a location or None for DNS riders.
        """
        locations = []
        current_time = RIDE_START_TIME
        while current_time <= RIDE_END_TIME:
            locations.append(int(self.get_location(current_time)))
            current_time += timedelta(minutes=15)

        return locations

    def get_location(self, when):
	"""
        Return the rider location at time WHEN.
        controls is a list of control objects,
        times is the list of checkpoint times for the rider.
	"""
	def rider_at_waypoint():
	    if waypoints[min].transition == Waypoint.TRANSITION_ARRIVAL and \
	       waypoints[max].transition == Waypoint.TRANSITION_DEPARTURE and \
	       waypoints[min].kilometers == waypoints[max].kilometers:
		    return True

	    return False

	waypoints = self.waypoints
	if not waypoints:
	    return None
	
        # Start control only - no data for positioning;
        if len(waypoints) == 1:
	    return waypoints[0].kilometers
	
	# Rider hasn't started yet;
	if when <= waypoints[0].timestamp:
	    return waypoints[0].kilometers
	
	# Past the final time for this rider;
	if when >= waypoints[-1].timestamp:
	    return waypoints[-1].kilometers

	min = 0
	max = len(waypoints) - 1
	while min+1 < max:
	    median = (min+max)/2
	    if when < waypoints[median].timestamp:
		max = median
	    else:
		min = median

        # Rider is still at a checkpoint
	if rider_at_waypoint():
	    return waypoints[min].kilometers

        ride_time = when - waypoints[min].timestamp
        time_between_waypoints = waypoints[max].timestamp - waypoints[min].timestamp
        distance_between_waypoints = waypoints[max].kilometers - waypoints[min].kilometers

        # Additional distance is  ride_time/time_between_breaks * distance_between_breaks
        extra_distance = (ride_time.total_seconds()/time_between_waypoints.total_seconds()) * distance_between_waypoints

        return waypoints[min].kilometers + extra_distance


class Waypoint(models.Model):

    TRANSITION_ARRIVAL = 1
    TRANSITION_DEPARTURE = 2

    SOURCE_SYSTEM = 1
    SOURCE_USER = 2
    SOURCE_SYNTHETIC = 3

    frame_key = models.ForeignKey(Rider)
    kilometers = models.FloatField()
    transition = models.IntegerField()  # 1 == arrival, 2 == departure;
    timestamp = models.DateTimeField()
    data_source = models.IntegerField()  # 1 == from system, 2 == user data;

    def __repr__(self):
        return "Waypoint(%d, %.1f, %s, %s, %d)" % (self.frame_key_id, self.kilometers, str(self.arrival), str(self.departure), self.data_source)
