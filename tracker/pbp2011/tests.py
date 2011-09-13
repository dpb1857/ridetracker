"""
PBP2011 tests.
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

    def setup_ordering(self):
        start, end = self.one_day()
        x = RiderTimeDelta(start, end)
        y = RiderTimeDelta(start, end, dnf=True)
        z = RiderTimeDelta(start, end, dns=True)
        return x, y, z

    def test_ordering1(self):
        """
        Tests ordering of RiderTimeDeltas.
        """
        x, y, z = self.setup_ordering()
        self.assertLess(x,  y)

    def test_ordering2(self):
        """
        Tests ordering of RiderTimeDeltas.
        """
        x, y, z = self.setup_ordering()
        self.assertLess(y,  z)

    def test_properties1(self):
        """
        Test that properties have the correct values.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end)
        self.assertEqual(x.days, 1)

    def test_properties2(self):
        """
        Test that properties have the correct values.
        """
        start, end = self.one_hour()
        x = RiderTimeDelta(start, end)
        self.assertEqual(x.seconds, 3600)

    def test_formatter1(self):
        """
        Test the format_ride_time() filter used by the templates.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end)
        self.assertEqual(format_ride_time(x), "24:00")
        
    def test_formatter2(self):
        """
        Test the format_ride_time() filter used by the templates.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end, dns=True)
        self.assertEqual(format_ride_time(x, show_special=True), "DNS")
        
    def test_formatter3(self):
        """
        Test the format_ride_time() filter used by the templates.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end, dns=True)
        self.assertEqual(format_ride_time(x, show_special=False), "")
        
    def test_formatter4(self):
        """
        Test the format_ride_time() filter used by the templates.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end, dnf=True)
        self.assertEqual(format_ride_time(x, show_special=True), "DNF")
        
    def test_formatter5(self):
        """
        Test the format_ride_time() filter used by the templates.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, end, dnf=True)
        self.assertEqual(format_ride_time(x, show_special=False), "")

    def test_formatter6(self):
        """
        Test the format_ride_time() filter used by the templates.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, None)
        self.assertEqual(format_ride_time(x, show_special=True), "Unknown")
        
    def test_formatter7(self):
        """
        Test the format_ride_time() filter used by the templates.
        """
        start, end = self.one_day()
        x = RiderTimeDelta(start, None)
        self.assertEqual(format_ride_time(x, show_special=False), "")


class ViewTest(TestCase):

    fixtures = ["fixtures/pbp2011_us_data.json.gz"]

    def test_exception_test(self):
        """
        Make sure our raise_exception view really raises an exception.
        """
        c = Client()
        with self.assertRaises(Exception):
            c.get("/raise_exception")

    def test_country_view(self):
        """
        Test that we can render the country view page.
        """
        c = Client()
        c.get('/pbp2011/country')

    def test_all_riders(self):
        """
        Test that we an render the list of all riders.
        """
        c = Client()
        c.get('/pbp2011/country/US')

    def test_country_riders(self):
        """
        Test that we an render the list of riders for a single country.
        """
        c = Client()
        resp = c.get('/pbp2011/country/US')

    def test_country_illegal(self):
        """
        Test that an unrecognized country returns a 404 page.
        """
        c = Client()
        resp = c.get('/pbp2011/country/xx')
        self.assertEqual(resp.status_code, 404)

    def test_country_illegal2(self):
        """
        Test that an unrecognized country returns a 404 page.
        """
        c = Client()
        resp = c.get('/pbp2011/country/xyz')
        self.assertEqual(resp.status_code, 404)

    def test_country_uk(self):
        """
        Test that a country code of 'uk' is ok.
        """
        c = Client()
        resp = c.get('/pbp2011/country/uk')
        self.assertEqual(resp.status_code, 301)
