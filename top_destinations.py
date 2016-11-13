#!/usr/bin/python

import requests
import os
import simplejson as json

TOP_DEST_BASE_URL='https://api.sandbox.amadeus.com/v1.2/travel-intelligence/top-destinations'
DEFAULT_PERIOD='2016-09'
DEFAULT_ORIGIN='NYC'
NUMBER_OF_RESULTS=5

def get_top_dest_url(origin):
  api_key = os.environ['AMADEUS_KEY']
  return '{0}?apikey={1}&period={2}&origin={3}&number_of_results={4}'.format(
           TOP_DEST_BASE_URL,
           api_key,
           DEFAULT_PERIOD,
           origin,
           NUMBER_OF_RESULTS)

def get_top_destinations(origin=DEFAULT_ORIGIN):
  print 'ORIGIN: ' + origin
  r = requests.get(get_top_dest_url(origin))
  if r.status_code != 200:
    return None
  else:
    amadeus_resp = json.loads(r.text)    
    print amadeus_resp
    resp = dict()
    resp['status'] = 'INTELLIGENCE'
    resp['message'] = 'The top areas to visit from {0} are: '.format(origin)
    for dest in amadeus_resp['results'][:-1]:
      resp['message'] += dest['destination'] + ', '
    resp['message'] += amadeus_resp['results'][-1]['destination']
    return resp

    

if __name__ == '__main__':
  print get_top_destinations()
