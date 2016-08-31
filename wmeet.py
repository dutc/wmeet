#!/usr/bin/env python3
from argparse import ArgumentParser
from dateutil.parser import parse
from datetime import datetime, timedelta
from pytz import all_timezones, timezone
from tzlocal import get_localzone
from itertools import islice, tee
from sys import stderr, exit, argv
from os.path import dirname, realpath, join
from math import copysign

nwise = lambda g,n=2: zip(*(islice(g,i,None) for i,g in enumerate(tee(g,n))))
def substr_tz(city):
    global timezones
    entry = timezones.get(city)
    tz = entry and timezone(entry)
    return city, tz

parser = ArgumentParser(description='Show meeting times in different locales.')
parser.add_argument('timezones', metavar='TZ', nargs='*', action='store',
                    type=substr_tz, help='the locales')
parser.add_argument('-t', '--time', metavar='TIME', dest='now', action='store',
                    type=parse, default=datetime.now(),
                    help='the base time (in the base locale)')
parser.add_argument('-r', '--r', dest='hours', action='store', type=int,
                    default=24, help='the number of hours to run')
parser.add_argument('-z', '--zone', metavar='ZONE', dest='base',
                    action='store', type=substr_tz,
                    default=('', get_localzone()), help='the base locale')

time_fmt = '{:%H:%M}'.format
date_fmt = '{:%a %d-%b %H:%M}'.format

if __name__ == '__main__':
    timezones = {}
    with open(join(dirname(realpath(__file__)), 'cities15000.txt')) as f:
        for row in (x.split('\t') for x in f):
            for name in row[3].split(','):
                timezones[name] = row[-2]
    args = parser.parse_args(argv[1:])
    if not all(tz for tzn,tz in args.timezones):
        bad_tzns = [tzn for tzn,tz in args.timezones if not tz]
        stderr.write('Cannot find locales: {}\n'.format(', '.join(bad_tzns)))
    base_tzn, base_tz = args.base
    if not base_tz:
        stderr.write('Cannot find base locale: {}\n'.format(base_tzn))
        exit(1)
    base_now = base_tz.localize(args.now)
    tzs = [base_tz] + [tz for tzn,tz in args.timezones if tz]
    base_times = [base_now.astimezone(tz) for tz in tzs]
    times = [[tz.normalize(base_time + timedelta(hours=n)) for n
             in range(0, args.hours, int(copysign(1,args.hours)))]
             for tz,base_time in zip(tzs,base_times)]
    fmts = [[date_fmt] +
            [time_fmt if prev.day == curr.day else date_fmt for prev,curr
             in nwise(ts)] for ts in times]
    row = ''.join('{:>18}' for _ in tzs).format
    print(row(*(tz.tzname(None) for tz in tzs)))
    print('\n'.join(row(*(f(t) for f,t in zip(fs,ts)))
                        for fs,ts in zip(zip(*fmts), zip(*times))))
