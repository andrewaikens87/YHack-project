from flask import Flask, render_template
from flask import jsonify
from flask import request
import json
import time
import jetblue as jb
import csv


app = Flask(__name__)

protocol = 'http://'
host = 'localhost'
port = '5000'

airplane_data = dict()
deals_dict = dict()
low_fares = dict()


@app.route('/')
def hello():
	if(len(deals_dict) == 0):
		runner()
	return render_template('index.html')

#Calls function on click of submit button
@app.route('/submit/', methods = ['POST'])
def submit():
	print(request.form)
	origin = request.form["origin"]
	dest = request.form["dest"]
	leftDate = request.form["departDate"]
	rightDate = request.form["returnDate"]
	if(len(deals_dict) == 0):
		runner()

	print(deals_dict[(origin,dest)])
	return render_template('index.html')

@app.route('/jetblue/index/')
def index():
	return render_template('index.html')

def results(target_flights):
	string = ''
	string += 'Average price in range: ${}\n'.format(jb.avgPrice(target_flights))

	string += 'Cheapest flight(s) in date range using USD: \n'
	for flight in jb.get_cheapest_flights(target_flights, True):
		string += '\t From: {} To: {} Date: {} Transfers: {} Score: {} Price: {} Tax: {}'.format(flight[1], flight[2],
			flight[3], flight[4], flight[5], flight[6], flight[7])

	string += 'Cheapest flight(s) in date range using points: \n'
	for flight in jb.get_cheapest_flights(target_flights, False):
		string += '\t From: {} To: {} Date: {} Transfers: {} Score: {} Price: {} Tax: {}'.format(flight[1], flight[2],
			flight[3], flight[4], flight[5], flight[6], flight[7])

	# string += 'Cheapest flight(s) regardless of date range using USD: \n'
	# for flight in jb.get_cheapest_flights(deals_dict[(target_flights[0][1], target_flights[0][2])], True):
	# 	string += '\t From: {} To: {} Date: {} Transfers: {} Score: {} Price: {} Tax: {}'.format(flight[1], flight[2],
	# 		flight[3], flight[4], flight[5], flight[6], flight[7])

	# string += 'Cheapest flight(s) regardless of date range using points: \n'
	# for flight in jb.get_cheapest_flights(deals_dict[(target_flights[0][1], target_flights[0][2])], False):
	# 	string += '\t From: {} To: {} Date: {} Transfers: {} Score: {} Price: {} Tax: {}'.format(flight[1], flight[2],
	# 		flight[3], flight[4], flight[5], flight[6], flight[7])

def runner():
	s = ""
	for line in open("airports.json"):
		s += line
	json_airplanes = json.loads(s)

	airplane_data = {i['code']: i for i in json_airplanes}
	first = True

	with open('Deals.csv', newline='') as deals:
		reader_deals = csv.reader(deals, delimiter=',', quotechar="\"")
		for row in list(reader_deals):
			if(first):
				first = False
				continue
			t = (row[1], row[2])
			if(t in deals_dict):
				deals_dict[t].add(tuple(row))
			else:
				deals_dict[t] = set()
				deals_dict[t].add(tuple(row))

	first = True
	with open('LowestFares.csv', newline='') as lowfares:
		reader_low = csv.reader(lowfares, delimiter=',', quotechar='\"')
		for row in list(reader_low):
			if(first):
				first = False
				continue
			t = (row[0], row[1])
			if(t in low_fares):
				low_fares[t].add(tuple(row))
			else:
				low_fares[t] = set()
				low_fares[t].add(tuple(row))

	#print(results(jb.process(deals_dict, low_fares, '12/2/2017', '1/31/2018', 'SFO', 'BOS')))

	#app.run()
