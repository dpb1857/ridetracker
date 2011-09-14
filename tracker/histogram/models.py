
import pickle
from datetime import datetime, timedelta

from django.db import models

from pbp2011.models import Checkpoint, Control

# Create your models here.

PBP2011_START_TIME = datetime(2011, 8, 21, 16, 0)
PBP2011_END_TIME = datetime(2011, 8, 25, 18, 0)

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
        num_columns = Control.get_num_controls()

        # Load up the rider data;
        for checkpoint in Checkpoint.objects.all():
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
    def get_location(controls, times, when):

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

    @staticmethod
    def compute_histogram(rider_data, time):

        controls = Control.get_controls()
        final_distance = int(controls[-1].distance)
        locations = [0] * (final_distance + 1)

        for row in rider_data.values():
            location = Location.get_location(controls, row, time)
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
    Location.compute_series(PBP2011_START_TIME, PBP2011_END_TIME)


