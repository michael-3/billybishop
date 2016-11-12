#!/usr/bin/python

import os
from amadeus import Flights
import simplejson as json
import sys

DEFAULT_ORIGIN = 'SFO'
DEFAULT_DEPARTURE_DATE = '2016-11-12'

def get_api_key():
  return os.environ['AMADEUS_KEY']

def get_flight_searcher():
  api_key = get_api_key()
  return Flights(api_key)

def find_flights(destination,
                 origin=DEFAULT_ORIGIN,
                 departure_date=DEFAULT_DEPARTURE_DATE):
  searcher = get_flight_searcher()
  return searcher.inspiration_search(
    destination=destination,
    origin=origin,
    departure_date=departure_date)

# for testing (for example: ./flight_finder.py BOM | python -m json.tool)
if __name__ == '__main__':
  print json.dumps(find_flights(sys.argv[1]))