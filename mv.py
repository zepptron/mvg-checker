#!/usr/bin/env python

from flask import Flask, render_template
import mvg_api
import os
import json

stations = json.loads(os.environ['MVG_CHECKER'])
template = "main.html"

def get_id(station):
	sid = mvg_api.get_id_for_station(station)
	return sid

def get_stuff(string):
	get = mvg_api.get_departures(get_id(string))
	summary = {}
	f=0
	for i in get:
		f=f+1
		summary[f] = {
			'label': i['label'],
			'product': i['product'],
			'destination': i['destination'],
			'departure': i['departureTimeMinutes']
		}
	return summary

app = Flask(__name__)

@app.route("/<any({}):segment>".format(str(stations)[1:-1]))
def first(segment):
	return render_template(
		template,
		title=segment,
		dict=get_stuff(segment),
		station=segment,
		stations=stations
	)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, use_reloader=True)
