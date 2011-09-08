#!/usr/bin/env python

import datetime
import itertools
import re
import StringIO
import urllib2

from lxml import etree

import pbp2011.models as models


def get_rider_times(rider_num):

    data = "code_tap=%04d" % rider_num
    u = urllib2.urlopen("http://www.paris-brest-paris.org/pbp2011/inscription/script/suivi_recup.php", data)
    data = u.read()
    u.close()

    match = re.search('innerHTML="(.*)";', data)
    table = match.group(1)
    table = table.replace('\\"', '"')
    table = table.replace("ABANDON</strong>", "ABANDON</strong></td>") # Fix bad html;
    table = table.replace("NON PARTANT</strong>", "NON PARTANT</strong></td>") # Fix bad html;
    dnf = True if table.find("ABANDON") >= 0  else False
    dns = True if  table.find("NON PARTANT") >= 0 else False

    parser = etree.XMLParser(recover=False, encoding="iso-8859-1")
    table_elem = etree.parse(StringIO.StringIO(table), parser)

    if 0:
        for i in itertools.count(2):
            row = table_elem.xpath("//tr[%d]" % i)[0]
            if len(row) < 2:
                break
            print row[0].text, row[1].text

    # If you like one-liners...
    # times = [(x[0].text, x[1].text) for x in itertools.takewhile(lambda x: len(x) >= 2, itertools.imap(lambda x: table.xpath("//tr[%d]" % x)[0], itertools.count(2)))]
    
    # Interate over the rows;
    row_iter = itertools.imap(lambda x: table_elem.xpath("//tr[%d]" % x)[0], itertools.count(2))
    
    # Stop when the row doesn't have enough td's
    row_iter = itertools.takewhile(lambda x: len(x) >= 2, row_iter)

    # Build tuples of control name and time
    data = [(x[0].text, x[1].text) for x in row_iter]
    
    return dnf, dns, data

def fixup_times(frame_num, times):
    
    if frame_num in (8402,):
        del times[0]

    if frame_num in (4346, 5620, 5646, 5719, 5943, 5949, 6937, 7039):
        del times[3]

    if frame_num in (2128, 2528, 4392, 5487, 5681, 5751, 7540, 8431, 8542):
        del times[4]

    if frame_num in (62, 1488, 2850, 4464, 4547, 4572, 5119, 5257, 5351, 5428, 5588, 6056, 7640, 8565):
        del times[5]

    if frame_num in (610, 2479, 2629, 2781, 2807, 4365, 4454, 4763, 4919, 5405, 5509, 5587, 6020, 7158):
        del times[6]

    if frame_num in (5891, 7712):
        del times[8]

    if frame_num in (7633,):
        del times[9]

    if frame_num in (5797,):
        del times[10]

    if frame_num in (589,):
        del times[11]

    if frame_num in (1712, 7511):
        del times[12]

    if frame_num in (8421,):
        del times[13]

    if frame_num in (7019,):
        del times[14]

    if frame_num == 589:
        times = times[:8] + [('LOUDEAC', '23-08 02:00')] + times[8:]

    if frame_num == 4464:
        times = times[:12] + [('MORTAGNE-AU-PERCHE', '24-08 17:31')] + times[12:]

    if frame_num == 5797:
        times = times[:13] + [('DREUX', '25-08 08:05')] + times[13:]

    if frame_num == 6020:
        times = times[:10] + [('FOUGERES', '24-08 08:11')] + times[10:]

    if frame_num == 7019:
        times = times[:8] + [('LOUDEAC', '23-08 07:38')] + times[8:]

    if frame_num == 7511: # From previously saved data;
        times = times[:13] + [('DREUX', '25-08 13:29')] + times[13:]

    if frame_num == 7633:
        times = times[:13] + [('DREUX', '25-08 02:37')] + times[13:]

    if frame_num == 7712:
        times = times[:11] + [('VILLAINES-LA-JUHEL', '25-08 07:00')] + times[11:]

    if frame_num == 8421:
        times = times[:7] + [('CARHAIX-PLOUGUER', '23-08 09:18')] + times[7:]


    return times


def process_rider_times(frame_num, dnf, dns, times):

    CONTROLS = {
        'SAINT-QUENTIN-EN-YVELINES': (1, 15),
        'VILLAINES-LA-JUHEL': (2, 12),
        'FOUGERES': (3, 11),
        'TINTENIAC': (4, 10),
        'LOUDEAC': (5, 9),
        'CARHAIX-PLOUGUER': (6, 8),
        'BREST': (7, 7),
        'MORTAGNE-AU-PERCHE': (13, 13),
        'DREUX': (14, 14),
        }

    try:
        control_obj = models.Control.get(frame_number=frame_num)
    except Exception:
        control_obj = models.Control(frame_number=frame_num)

    control_obj.dnf = dnf
    control_obj.dns = dns

    current_control = 0
    for control_name, time in times:
        ctl_low, ctl_hi = CONTROLS[control_name]

        if time == "26-08 10:40":
            continue

        # We've examined the replicated line issues...
        if False: 
            if ctl_low == current_control:
                print frame_num, "REPLICATED LINE:"
                continue

        new_control = ctl_low if current_control < ctl_low else ctl_hi
        if new_control - current_control >= 2:
            print frame_num, "MISSING CONTROLS:", new_control - current_control - 1

        if new_control < current_control:
            print frame_num, "STRANGE SEQUENCE ERROR"

        current_control = new_control
        attr = "cp%d" % current_control
        dt = datetime.datetime.strptime("2011-"+time, "%Y-%d-%m %H:%M")
        setattr(control_obj, attr, dt)

    control_obj.save()

def process_riders():

    riders = models.Rider.objects.all()
    for rider in riders:
        # print "Processing", rider.frame_number
        try:
            dnf, dns, times = get_rider_times(rider.frame_number)
            times = fixup_times(rider.frame_number, times)
            process_rider_times(rider.frame_number, dnf, dns, times)
        except:
            pass


def process_rider(frame_num):
    
    print "Processing", frame_num
    dnf, dns, times = get_rider_times(frame_num)
    print "times:", times
    times = fixup_times(frame_num, times)
    print "after fixup:", times
    process_rider_times(frame_num, dnf, dns, times)


if __name__ == "__main__":
    
    # process_riders()
    process_rider(8354)
