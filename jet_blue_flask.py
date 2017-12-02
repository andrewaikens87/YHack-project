from flask import Flask
from flask import jsonify
from flask import request
import json
import time
import jetblue as jb
import csv


app = Flask(__name__)

airplane_data = dict()
deals_dict = dict()
low_fares = dict()


@app.route('/')
def hello():
	return 'Hello World!'

#Calls function on click of submit button
@app.route('/submit/', methods = ['POST'])
def submit():
	content = request.get_json()
	output = jb.process(content['start_date_range'], content['return_date_range'], content['airport_code'])
	return jsonify(output)


if __name__ == '__main__':
	s = ""
	for line in open("airports.json"):
		s += line
	json_airplanes = json.loads(s)

	airplane_data = {i['code']: i for i in json_airplanes}

	with open('Deals.csv', newline='') as deals:
		reader_deals = csv.reader(deals, delimiter=',', quotechar='|')
		for row in reader_deals:
			t = (row[0], row[1])
			if(t in deals):
				deals_dict[t].add(tuple(row))
			else:
				deals_dict[t] = set()

	with open('LowestFares.csv', newline='') as lowfares:
		reader_low = csv.reader(lowfares, delimiter=',', quotechar='|')
		for row in reader_low:
			t = (row[0], row[1])
			if(t in low_fares):
				low_fares[t].add(tuple(row))
			else:
				low_fares[t] = set()


	app.run()
