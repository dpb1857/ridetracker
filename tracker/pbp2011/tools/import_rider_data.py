#!/usr/bin/env python

import urllib2

from lxml import html

import pbp2011.models as models

def get_rider_info(dossier):

    data = "rch=1&rch_num=%d" % dossier
    u = urllib2.urlopen("http://www.paris-brest-paris.org/pbp2011/index2.php?lang=fr&cat=randonnee&page=suivi_participants", data)
    data = u.read()
    u.close()

    tree = html.document_fromstring(data)
    rider_info = [element.text for element in tree.xpath("//table[2]/tr[2]/td")]
    return rider_info


def process_rider(info):

    country_str, last_name, first_name, bike_type_str, frame_number_str = info

    try:
        country = models.Country.objects.get(country_code=country_str)
    except Exception:
        country = models.Country(country_code=country_str)
        country.save()

    try:
        bike_type = models.BikeType.objects.get(bike_type=bike_type_str)
    except Exception:
        bike_type = models.BikeType(bike_type=bike_type_str)
        bike_type.save()

    r = models.Rider(frame_number=int(frame_number_str),
                     first_name=first_name,
                     last_name=last_name,
                     country=country,
                     bike_type=bike_type)
    r.save()


def main():
    for dossier in range(6000):
        print "processing dossier", dossier
        data = get_rider_info(dossier)
        if data: 
            process_rider(data)

if __name__ == "__main__":
    main()
