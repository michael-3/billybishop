#!/usr/bin/env python

from amadeus import Flights
from parser import get_route, get_departure
import csv
import os
import simplejson as json
import sys


def load_iata_codes():
    """Loads city->airport code mappings from cities.csv."""
    codes = {}
    with open('cities.csv') as f:
        for (city, airport) in csv.reader(f):
            codes[city] = airport
    return codes


IATA_CODES = load_iata_codes()


DEFAULT_ORIGIN = 'SFO'
DEFAULT_DEPARTURE_DATE = '2016-11-12'
NUM_RESULTS = 10


def get_api_key():
    return os.environ['AMADEUS_KEY']


def get_flight_searcher():
    api_key = get_api_key()
    return Flights(api_key)


def find_flights(message):
    """Parses the message and returns low fare flights."""
    origin = None
    destination = None
    departure_date = None

    route = get_route(message)
    origin = route.get('origin', None)
    destination = route.get('destination', None)

    print destination
    print message

    departure_date = get_departure(message)

    if departure_date:
        departure_date = departure_date['departure']

    if not (departure_date and origin and destination):
        return reask(
            departure_date is not None,
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
        departure_date=departure_date,
        number_of_results=NUM_RESULTS)


def reask(time_provided, destination_provided, origin_provided):
    """Returns a message that prompts for missing information."""
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
