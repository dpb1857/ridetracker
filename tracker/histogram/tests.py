"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import timedelta

import models

from django.test import TestCase


class HistogramTest(TestCase):
    
    fixtures = ["fixtures/pbp2011_us_data.json.gz", "fixtures/control_data.json.gz"]

    def test_aggregation(self):

        models.Location.aggregate_rider_data()

    def test_histogram(self):

        data = models.Location.aggregate_rider_data()
        locations = models.Location.compute_histogram(data, models.PBP2011_START_TIME + timedelta(hours=5))

    def test_series(self):

        start = models.PBP2011_START_TIME
        end = start + timedelta(hours=2)
        models.Location.compute_series(start, end)

