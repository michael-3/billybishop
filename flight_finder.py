#!/usr/bin/python

import os
from amadeus import Flights
import simplejson as json
import sys
from parser import get_route, get_departure

IATA_CODES = {
  'new_york_city': 'NYC',
  'chicago': 'CHI',
  'los_angeles': 'LAX',
  'houston': 'HOU',
  'san_fransisco': 'SFO'
}


DEFAULT_ORIGIN = 'SFO'
DEFAULT_DEPARTURE_DATE = '2016-11-12'
NUM_RESULTS = 10

def get_api_key():
  return os.environ['AMADEUS_KEY']

def get_flight_searcher():
  api_key = get_api_key()
  return Flights(api_key)


def find_flights(message):


  origin = None
  destination = None
  time = None

  route = get_route(message)
  origin = route.get('origin', None)
  destination = route.get('destination', None)

  print destination

  print message
  time = get_departure(message)

  if time:
    time = time['departure']

 
  if not (time and origin and time):
    return reask(time is not None,
                 destination is not None,
                 origin is not None)


  if origin.lower() in IATA_CODES:
    origin = IATA_CODES[origin.lower()]
  if destination.lower() in IATA_CODES:
    destination = IATA_CODES[destination.lower()]
  searcher = get_flight_searcher()

  return searcher.low_fare_search(
    destination=destination,
    origin=origin,
    departure_date=time,
    number_of_results=NUM_RESULTS)


def reask(time_provided, destination_provided, origin_provided):
  mapping = {
    (False, False, False): 'Please provide flight details',
    (False, False, True): 'Please provide destination and departure date',
    (False, True, False): 'Please provide origin and departure date',
    (True, False, False): 'Please provide origin and destination',
    (False, True, True): 'Please provide departure time',
    (True, False, True): 'Please provide destination',
    (True, True, False): 'Please provide origin'
  }
  return mapping[(time_provided, destination_provided, origin_provided)]
 


# for testing (for example: ./flight_finder.py BOM | python -m json.tool)
if __name__ == '__main__':
  print json.dumps(find_flights(sys.argv[1]))
