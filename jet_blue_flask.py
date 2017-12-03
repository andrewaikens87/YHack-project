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
	origin = request.form["origin"]
	dest = request.form["dest"]
	leftDate = request.form["departDate"]
	rightDate = request.form["returnDate"]
	if(len(deals_dict) == 0):
		runner()

	print(deals_dict[(origin,dest)])
	target_flights = jb.process(deals_dict, low_fares, leftDate, rightDate, origin, dest)

	results_list = results(target_flights)
	return render_template('result_page.html', average = results_list[0], minInRangeDollars = results_list[1], minInRangePoints = results_list[2],
		minOutOfRangeDollars = results_list[3], minOutOfRangePoints = results_list[4], domVsInt = results_list[5], getAway = results_list[6])

@app.route('/jetblue/index/')
def index():
	return render_template('index.html')

def results(target_flights):
	string = ''
	string += 'Average price in range: ${}\n'.format(jb.avgPrice(target_flights))
	results = []

	average = jb.avgPrice(target_flights)
	results.append(average)

	string += 'Cheapest flight(s) in date range using USD: \n'

	flight_list = jb.get_cheapest_flights(target_flights[0], True)
	s1 = ''
	for flight in flight_list:
		s1 += "\tFrom {} to {} on {} with a score of {} | Price: ${} + Tax: ${}\n".format(flight[1],
			flight[2], flight[3], flight[6], flight[7], flight[8])
	results.append(s1)
	
	flight_list_2 = jb.get_cheapest_flights(target_flights[0], False)
	s1 = ''
	for flight in flight_list_2:
		s1 += "\tFrom {} to {} on {} with a score of {} | Points from fare: {} + Points from tax: {}\n".format(flight[1],
			flight[2], flight[3], flight[6], flight[9], flight[10])
	results.append(s1)
		
	flight_list_3 = jb.get_cheapest_flights(deals_dict[(target_flights[0][0][1], target_flights[0][0][2])], True)
	s1 = ''
	for flight in flight_list_3:
		s1 += "\tFrom {} to {} on {} with a score of {} | Price: ${} + Tax: ${}\n".format(flight[1],
			flight[2], flight[3], flight[6], flight[7], flight[8])
	results.append(s1)

	flight_list_4 = jb.get_cheapest_flights(deals_dict[(target_flights[0][0][1], target_flights[0][0][2])], False)
	s1 = ''
	for flight in flight_list_4:
		s1 += "\tFrom {} to {} on with a score: {} | Points from fare: {} + Points from tax: {}\n".format(flight[1],
			flight[2], flight[3], flight[6], flight[9], flight[10])
	results.append(s1)

	results.append(jb.domestic_vs_international(low_fares))

	results.append(jb.get_away(deals_dict, low_fares, target_flights[0][0][1]))
	return results

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