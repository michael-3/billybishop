#!/usr/bin/env python

import sys
import dateutil.parser as dparser
from nltk.tokenize.mwe import MWETokenizer
import csv


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
    date_time = dparser.parse(msg, fuzzy=True, yearfirst=True)
    departure = {'departure': str(date_time.date())}
    return departure


if __name__ == '__main__':
    msg = sys.argv[1]
    print get_route(msg), get_departure(msg)
