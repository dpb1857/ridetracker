
import pickle
from datetime import datetime, timedelta

from django.db import models

import pbp2011.models as ridemodels

# Create your models here.

class Location(models.Model):
    time = models.DateTimeField(primary_key=True)
    histogram = models.TextField()

    @staticmethod
    def aggregate_rider_data():
        """
        Load rider data, return a dict where
        rider_data[frame_num] is a row of control times for a rider;
        """
        
        rider_data = {}
        num_columns = ridemodels.Control.get_num_controls()

        # Load up the rider data;
        for checkpoint in ridemodels.Checkpoint.objects.all():
            rider_row = rider_data.get(checkpoint.frame_number, None)
            if rider_row is None:
                rider_row = [None] * num_columns
                rider_data[checkpoint.frame_number] = rider_row

            rider_row[checkpoint.checkpoint_number-1] = checkpoint.time

        # Trim trailing Nones off each row;
        for frame_num, row in rider_data.items():
            while(row[-1] is None):
                del row[-1]
                
            # XXX for now, nuke entries with missing internal control values;
            for i in row:
                if i is None:
                    del rider_data[frame_num]
                    break
            
        return rider_data

    @staticmethod
    def compute_histogram(rider_data, time):

        controls = ridemodels.Control.get_controls()
        final_distance = int(controls[-1].distance)
        locations = [0] * (final_distance + 1)

        for row in rider_data.values():
            location = ridemodels.Rider.get_location(time, controls, row)
            locations[int(location)] += 1
    
        return locations

    @staticmethod
    def compute_series(start, end, step=timedelta(minutes=15)):

        rider_data = Location.aggregate_rider_data()
        current_time = start
        while current_time <= end:
            locations = Location.compute_histogram(rider_data, current_time)
            loc = Location(current_time, pickle.dumps(locations))
            loc.save()
            current_time += step

def compute_pbp2011_histogram():

    Location.objects.all().delete()
    Location.compute_series(ridemodels.RIDE_START_TIME, ridemodels.RIDE_END_TIME)


