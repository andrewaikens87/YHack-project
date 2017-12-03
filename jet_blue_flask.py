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
	output = jb.process(content['start_date_range'], content['depart_airport_code'], content['dest_airport_code'])
	return jsonify(output)

if __name__ == '__main__':
	s = ""
	for line in open("airports.json"):
		s += line
	json_airplanes = json.loads(s)

	airplane_data = {i['code']: i for i in json_airplanes}
	first = True

	with open('Deals.csv', newline='') as deals:
		reader_deals = csv.reader(deals, delimiter=',', quotechar="|")
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

	i = 0
	input_array = []
	while(i < 4):
		input_string = str(input())
		input_array.append(input_string)
		i += 1
		if(i == 4):
			#print(jb.process(deals_dict, low_fares, input_array[0], input_array[1], input_array[2], input_array[3]))
			i = 0
			print((jb.get_away(deals_dict, low_fares, input_array[2]))[0], (jb.get_away(deals_dict, low_fares, input_array[2]))[1], (jb.get_away(deals_dict, low_fares, input_array[2]))[2])
		if(input_string == "quit"):
			break

	app.run()
