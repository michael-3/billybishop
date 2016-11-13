#!/usr/bin/env python

from nltk.tokenize.mwe import MWETokenizer
import csv
import dateutil.parser as dparser
import sys
import spacy
from spacy.symbols import dobj, pobj, GPE, VERB, ADP


def load_city_tokens():
    """Loads tokens to use with MWETokenizer from cities.csv."""
    tokens = []
    with open('cities.csv') as f:
        for (city, _) in csv.reader(f):
            tokens.append(tuple(city.split('_')))
    return tokens


CITY_TOKENS = load_city_tokens()

def get_route2(msg):
	nlp = spacy.load('en')
	doc = nlp(msg.title().decode('utf-8'))
	nlp.parser(doc)
	
	#merged entities ('New', 'York', 'City') -> ('New York City')
	for ent in doc.ents:
		doc.merge(ent.start_char, ent.end_char)
	
	route = {'origin' : None, 'destination' : None}
	
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
    print get_route2(msg), get_departure(msg)
