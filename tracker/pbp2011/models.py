
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

    @property
    def days(self):
        
        return self.timedelta.days

    @property
    def seconds(self):

        return self.timedelta.seconds



# class RiderTimeDelta(object):
#     
#     def  __init__(self, start, end):
# 
#         try:
#             self.delta = end - start
#         except Exception:
#             self.delta = None
#     
#     def __str__(self):
#         
#         return self.__unicode__()
# 
#     def __unicode__(self, fmt="%d:%02d"):
# 
#         if self.delta is None:
#             return ""
#         hours = self.delta.days*24 + self.delta.seconds/3600
#         mins = (self.delta.seconds % 3600)/60
#         return fmt % (hours, mins)
# 
# 
# class RiderTotalTime(object):
# 
#     def __init__(self, start, end, dns=False, dnf=False):
#         self.dns = dns
#         self.dnf = dnf
#         self.delta = RiderTimeDelta(start, end) if start and end else None
# 
#         if self.dns:
#             self.print_value = u'DNS'
#             self._sort_key = u'DNS'
#         elif self.dnf:
#             self.print_value = u'DNF'
#             self._sort_key =  u'DNF'
#         elif self.delta is None:
#             self.print_value = u'Unknown'
#             self._sort_key = u'Unknown'
#         else:
#             self.print_value = unicode(self.delta)
#             self._sort_key = self.delta.__unicode__(fmt="%03d:%02d")
#             
#     def __str__(self):
# 
#         return self.print_value
# 
# 
#     def __unicode__(self):
#         
#         return self.print_value
# 
#     @property
#     def sort_key(self):
#         
#         return self._sort_key


class BikeType(models.Model):
    bike_type = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.bike_type

class Rider(models.Model):
    frame_number = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    country = CountryField()
    bike_type = models.ForeignKey(BikeType)

    dnf = models.BooleanField(default=False) 
    dns = models.BooleanField(default=False) 
    cp1 = models.DateTimeField(null=True) # SQY
    cp2 = models.DateTimeField(null=True) # Villaines
    cp3 = models.DateTimeField(null=True) # Fougeres
    cp4 = models.DateTimeField(null=True) # Tinteniac
    cp5 = models.DateTimeField(null=True) # Loudeac
    cp6 = models.DateTimeField(null=True) # Carhaix
    cp7 = models.DateTimeField(null=True) # Brest
    cp8 = models.DateTimeField(null=True) # Carhaix
    cp9 = models.DateTimeField(null=True) # Loudeac
    cp10 = models.DateTimeField(null=True) # Tinteniac
    cp11 = models.DateTimeField(null=True) # Fougeres
    cp12 = models.DateTimeField(null=True) # Villaines
    cp13 = models.DateTimeField(null=True) # Mortagne
    cp14 = models.DateTimeField(null=True) # Dreux
    cp15 = models.DateTimeField(null=True) # SQY

    def __unicode__(self):
        return "%d %s %s" % (self.frame_number, self.first_name, self.last_name)

    @property
    def elapsed(self):
        return RiderTimeDelta(self.cp1, self.cp15, dns=self.dns, dnf=self.dnf)


for cls in BikeType, Rider:
    try:
        admin.site.register(cls)
    except Exception:
        pass
