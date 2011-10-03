
import pickle
from datetime import datetime, timedelta

from django.db import models

import pbp2011.models as ridemodels

# Create your models here.

class Location(models.Model):
    time = models.DateTimeField(primary_key=True)
    histogram = models.TextField()

    @staticmethod
    def compute_histogram(riders, time):

        controls = ridemodels.Control.get_controls()
        final_distance = int(controls[-1].distance)
        locations = [0] * (final_distance + 1)
        dnfs = [0] * (final_distance + 1)

        for rider in riders:
            location = rider.get_location(time)
            if location is not None:
                kilometers = int(location[0])
                if location[1]:
                    locations[kilometers] += 1
                else:
                    dnfs[kilometers] += 1
    
        return locations, dnfs

    @staticmethod
    def compute_series(start, end, step=timedelta(minutes=15)):

        riders = ridemodels.Rider.objects.all()

        current_time = start
        while current_time <= end:
            locations, dnfs = Location.compute_histogram(riders, current_time)
            loc = Location(current_time, pickle.dumps((locations, dnfs)))
            loc.save()
            current_time += step

    @staticmethod
    def get_histogram_data(time):
        """
        Returns: locations, dnfs
        """
        location = Location.objects.get(time=time)
        return pickle.loads(str(location.histogram))

def compute_pbp2011_histogram():

    Location.objects.all().delete()
    Location.compute_series(ridemodels.RIDE_START_TIME, ridemodels.RIDE_END_TIME)


