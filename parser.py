import sys
import dateutil.parser as dparser
from nltk import word_tokenize

def get_route(tokens):
	route = {}
	for i in xrange(len(tokens)):
		# fuzzy matching here?
		if tokens[i] == 'from':
			route['origin'] = tokens[i+1]
		if tokens[i] == 'to':
			route['destination'] = tokens[i+1]
	return route

def get_departure(msg):
	date_time = dparser.parse(msg, fuzzy=True, yearfirst=True)
	departure = {'departure' : str(date_time.date())}
	return departure
	

if __name__ == '__main__':
	msg = sys.argv[1]
	text = msg.split(" ")
	print get_route(text), get_departure(msg)
