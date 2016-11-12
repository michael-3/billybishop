import sys
import dateutil.parser as dparser
from nltk.tokenize.mwe import MWETokenizer

# returns a map of {'origin' : departure_location, 'destination' : arrival_location}
def get_route(msg):
	split = msg.split(" ")
	tokenizer = MWETokenizer([('san','francisco'), ('hong','kong'), ('new','york')])
	route = {'origin' : None, 'destination' : None}
	tokens = tokenizer.tokenize(split)
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
	print get_route(msg), get_departure(msg)
