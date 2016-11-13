#!/usr/bin/env python

from ctypes import cdll, c_char_p
from nltk.tokenize.mwe import MWETokenizer
import csv
import dateutil.parser as dparser
import os
import sys
import spacy
from spacy.symbols import dobj, pobj, GPE, VERB, ADP


def load_city_tokens():
    """Loads tokens to use with MWETokenizer from cities.csv."""
    cities = []
    tokens = []
    with open('cities.csv') as f:
        for (city, _) in csv.reader(f):
            cities.append(city)
            tokens.append(tuple(city.split('_')))
    return cities, tokens


def load_libfuzzy():
    """Checks that libfuzzy.so exists and loads it."""
    name = 'libfuzzy.so'
    if os.path.isfile(name):
        return cdll.LoadLibrary(name)

    print "Missing libfuzz.so. Please run build.sh."
    sys.exit(1)


def list_to_c_string_array(string_list):
    """Converts a Python list of strings to an array of C-style strings."""
    return (c_char_p * len(string_list))(*string_list)


CITIES, CITY_TOKENS = load_city_tokens()
CITIES_ARRAY = list_to_c_string_array(CITIES)
FUZZY = load_libfuzzy()
TOKEN_LOOKAHEAD = 3


def determine_city(tokens):
    """Attempts to determine the desired city using fuzzy matching."""
    if tokens[0] in CITIES:
        return tokens[0]

    guesses = [tokens[0]]
    for i in xrange(1, len(tokens)):
        guesses.append(guesses[-1] + '_' + tokens[i])
    guesses_array = list_to_c_string_array(guesses)

    index = FUZZY.match(
        guesses_array, len(guesses_array),
        CITIES_ARRAY, len(CITIES_ARRAY))
    if index >= 0:
        return CITIES[index]

    return None


def get_route2(msg):
    """Returns a map with keys 'origin' and 'destination'"""
    nlp = spacy.load('en')
    doc = nlp(msg.title().decode('utf-8'))
    nlp.parser(doc)

    # merged entities ('New', 'York', 'City') -> ('New York City')
    for ent in doc.ents:
        doc.merge(ent.start_char, ent.end_char)

    route = {'origin': None, 'destination': None}

    for w in doc:
        if (w.dep == pobj and w.head.pos == ADP and w.ent_type == GPE):
            if w.head.lower_ == 'to':
                route['destination'] = w.lower_
            else:
                route['origin'] = w.lower_
        elif (w.dep == dobj and w.head.pos == VERB and w.ent_type == GPE):
            route['origin'] = w.lower_
    return route


def get_route(msg):
    """Returns a map with keys 'origin'" and 'arrival_location'."""
    tokenizer = MWETokenizer(CITY_TOKENS)
    route = {'origin': None, 'destination': None}
    tokens = tokenizer.tokenize(msg.lower().split(' '))

    def lookahead(start_idx):
        """Returns a slice of the tokens list starting at index start_idx."""
        end_idx = min(start_idx + TOKEN_LOOKAHEAD, len(tokens))
        words = ['from', 'to', 'on']
        for i in xrange(start_idx + 1, end_idx):
            if tokens[i] in ['from', 'to', 'on']:
                end_idx = i
                break
        return tokens[start_idx:end_idx]

    for i in xrange(len(tokens) - 1):
        if tokens[i] in ['from', 'to']:
            city_tokens = lookahead(i + 1)
            city = determine_city(city_tokens)
            if city is None:
                print "City not recognized: {}".format(' '.join(city_tokens))
            else:
                if tokens[i] == 'from':
                    route['origin'] = city
                elif tokens[i] == 'to':
                    route['destination'] = city
    return route


def get_departure(msg):
    try:
        """Parses a date somewhere in msg and returns
           a map with key 'departure'."""
        date_time = dparser.parse(msg, fuzzy=True, yearfirst=True, default=datetime.datetime(1900,1,1))
        if date_time == datetime.datetime(1900,1,1):
          return None
    except ValueError:
        return None
    departure = {'departure': str(date_time.date())}
    return departure


if __name__ == '__main__':
    msg = sys.argv[1]
    print get_route(msg), get_departure(msg)
    #print get_route2(msg), get_departure(msg)
