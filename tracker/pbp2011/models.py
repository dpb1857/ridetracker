from django.db import models
from django.contrib import admin

from django_countries import CountryField

# Create your models here.

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
        
        class Elapsed(object):
            
            def __init__(self, dns, dnf, start, end):
                self.dns = dns
                self.dnf = dnf
                self.start = start
                self.end = end

            def __unicode__(self):
                return self.format_elapsed("%d:%02d")

            def format_elapsed(self, format):

                if self.dns: 
                    return "DNS"
                if self.dnf:
                    return "DNF"
                if self.end is None or self.start is None:
                    return "Unknown"

                delta = self.end - self.start
                hours = delta.days*24 + delta.seconds/3600
                mins = (delta.seconds % 3600)/60
                return format % (hours, mins)

            @property
            def sort_key(self):
                return self.format_elapsed("%03d:%02d")

        return Elapsed(self.dns, self.dnf, self.cp1, self.cp15)


for cls in BikeType, Rider:
    try:
        admin.site.register(cls)
    except Exception:
        pass
