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


def find_flights(message, origin=None, destination=None, departure_date=None):
    """Parses the message and returns low fare flights."""
    route = get_route(message)
    
    if 'origin' in route and route['origin']:
      origin = route['origin']
    if 'destination' in route and route['destination']:
      destination = route['destination']

    if get_departure(message):
      departure_date = get_departure(message)['departure']

    if not (departure_date and origin and destination):
        return reask(
            departure_date,
            destination,
            origin)

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


def reask(departure_date, destination, origin):
    """Returns a message that prompts for missing information."""
    response = {}

    if (not departure_date) and (not destination) and (not origin):
        response['message'] = 'Let us know your travel plans!'
    elif (not departure_date) and (not destination) and origin:
        response['message'] = 'Where do you want to go from {0}, and when are you leaving?'.format(origin)
    elif (not departure_date) and destination and (not origin):
        response['message'] = 'Nice, {0} is great this time of year! When are you leaving, and where from?'.format(destination)
    elif departure_date and (not destination) and (not origin):
        response['message'] = 'That\'s a good time for a trip! Where are you travelling between?'
    elif (not departure_date) and destination and origin:
        response['message'] = 'Sounds like a great trip! When would you like to leave?'
    elif departure_date and (not destination) and origin:
        response['message'] = 'Where are you planning to go?'
    elif departure_date and destination and (not origin):
        response['message'] = 'That\'s a great time to visit {0}! Where will you be departing from?'.format(destination)

    if departure_date:
        response['departure_date'] = departure_date
    if destination:
        response['destination'] = destination
    if origin:
        response['origin'] = origin

    response['status'] = 'FAILURE'

    return response

# for testing (for example: ./flight_finder.py BOM | python -m json.tool)
if __name__ == '__main__':
    print json.dumps(find_flights(sys.argv[1]))
