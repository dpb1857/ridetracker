"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import timedelta

import models

import pbp2011.models as ridemodels

from django.test import TestCase, Client


class HistogramTest(TestCase):
    
    fixtures = ["fixtures/pbp2011_us_data.json.gz", "fixtures/control_data.json.gz"]

    def test_histogram(self):

        riders = ridemodels.Rider.objects.all()
        locations = models.Location.compute_histogram(riders, ridemodels.RIDE_START_TIME + timedelta(hours=5))

    def test_series(self):

        start = ridemodels.RIDE_START_TIME
        end = start + timedelta(hours=2)
        models.Location.compute_series(start, end)

class ViewTest(TestCase):

    fixtures = ["fixtures/pbp2011_us_data.json.gz", "fixtures/control_data.json.gz"]

    def test_hist_data(self):

        c = Client()
        c.get("/histogram/histdata/2011-08-22 06:00")
    
    def test_frame_data(self):

        c = Client()
        c.get("/histogram/framedata/4484")

    def test_frame_data_bad_framenum(self):

        c = Client()
        c.get("/histogram/framedata/12345");
