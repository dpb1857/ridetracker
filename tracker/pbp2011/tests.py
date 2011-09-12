"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest

from datetime import datetime
from django.test import Client, TestCase

from models import RiderTimeDelta
from jinja2filters import format_ride_time

class RiderTimeDeltaTest(TestCase):

    @staticmethod
    def one_day():
        start = datetime(2000, 1, 1)
        end = datetime(2000, 1, 2)
        return start, end

    @staticmethod
    def one_hour():
        start = datetime(2000, 1, 1, 0)
        end = datetime(2000, 1, 1, 1)
        return start, end

    def test_ordering(self):
        """
        Tests ordering of RiderTimeDeltas.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end)
        y = RiderTimeDelta(start, end, dnf=True)
        z = RiderTimeDelta(start, end, dns=True)

        self.assertLess(x,  y)
        self.assertLess(y,  z)

    def test_properties(self):
        """
        Test that properties have the correct values.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end)
        self.assertEqual(x.days, 1)

        start, end = self.one_hour()
        x = RiderTimeDelta(start, end)
        self.assertEqual(x.seconds, 3600)

    def test_formatter(self):
        
        start, end = self.one_day()
        x = RiderTimeDelta(start, end)
        self.assertEqual(format_ride_time(x), "24:00")
        
        x = RiderTimeDelta(start, end, dns=True)
        self.assertEqual(format_ride_time(x, show_special=True), "DNS")
        
        x = RiderTimeDelta(start, end, dns=True)
        self.assertEqual(format_ride_time(x, show_special=False), "")
        
        x = RiderTimeDelta(start, end, dnf=True)
        self.assertEqual(format_ride_time(x, show_special=True), "DNF")
        
        x = RiderTimeDelta(start, end, dnf=True)
        self.assertEqual(format_ride_time(x, show_special=False), "")

        x = RiderTimeDelta(start, None)
        self.assertEqual(format_ride_time(x, show_special=True), "Unknown")
        
        x = RiderTimeDelta(start, None)
        self.assertEqual(format_ride_time(x, show_special=False), "")

if 0:
    class ViewTest(TestCase):

        def test_country_view(self):
            """
            Test that we can render the country view page.
            """
            c = Client()
            c.get('/pbp2011/country')
            # c.get('/pbp2011/country/US')
