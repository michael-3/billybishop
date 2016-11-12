#!/usr/bin/env python

from flask import Flask, render_template, request
from flight_finder import find_flights
import simplejson as json


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def main_app():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    return json.dumps(find_flights(request.args.get('query')))


if __name__ == '__main__':
    app.run()
