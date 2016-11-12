#!/usr/bin/env python

from nltk.tokenize.mwe import MWETokenizer
import csv
import dateutil.parser as dparser
import sys


def load_city_tokens():
    """Loads tokens to use with MWETokenizer from cities.csv."""
    tokens = []
    with open('cities.csv') as f:
        for (city, _) in csv.reader(f):
            tokens.append(tuple(city.split('_')))
    return tokens


CITY_TOKENS = load_city_tokens()


def get_route(msg):
    """Returns a map with keys 'origin'" and 'arrival_location'."""
    tokenizer = MWETokenizer(CITY_TOKENS)
    route = {'origin': None, 'destination': None}
    tokens = tokenizer.tokenize(msg.split(' '))
    for i in xrange(len(tokens) - 1):
        # fuzzy matching here?
        if tokens[i] == 'from':
            route['origin'] = tokens[i+1]
        if tokens[i] == 'to':
            route['destination'] = tokens[i+1]
    return route


def get_departure(msg):
    try:
        """Parses a date somewhere in msg and returns
           a map with key 'departure'."""
        date_time = dparser.parse(msg, fuzzy=True, yearfirst=True)
    except ValueError:
        return None
    departure = {'departure': str(date_time.date())}
    return departure


if __name__ == '__main__':
    msg = sys.argv[1]
    print get_route(msg), get_departure(msg)
