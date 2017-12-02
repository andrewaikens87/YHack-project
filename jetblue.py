import json
import datetime
import csv

def getAllFlightsForOriginAndDestination(airport_data, origin, destination):
	return

def getLowestPrice():
	return

def getAirportData(airport_data, name):
	return airport_data[name]

def avgPrice(data):
	cost_dollar = 0
	cost_points = 0
	valid_flights_dollar = 0
	valid_flights_points = 0
	for flight in data:
		if flight[4] == 'LOWEST':
			cost_dollar += flight[5]
			valid_flights_dollar += 1
		elif flight[4] == 'POINTS':
			cost_points += flight[5]
			valid_flights_points +=1
	return (0 if(valid_flights_dollar == 0) else cost_dollar/valid_flights_dollar, 0 if(valid_flights_points == 0) else cost_points/valid_flights_points)


	
#Takes in dates as strings
def is_in_date_range(start, end, target):
	uses_slashes = False
	uses_dashes = False


	if start.find('/') != -1:
		uses_slashes = True
	elif start.find('-') != -1:
		uses_dashes = True

	if uses_dashes:
		start = start.split('-')
		end = end.split('-')
		target = target.split('-')

		start_date = datetime.date(int(start[0]), int(start[1]), int(start[2][:2]))
		end_date = datetime.date(int(end[0]), int(end[1]), int(end[2][:2]))
		target_date = datetime.date(int(target[0]), int(target[1]), int(target[2][:2]))

	elif uses_slashes: 
		start = start.split('/')
		end = end.split('/')
		target = target.split('/')

		start_date = datetime.date(int(start[2][:4]), int(start[1]), int(start[0]))
		end_date = datetime.date(int(end[2][:4]), int(end[1]), int(end[0]))
		target_date = datetime.date(int(target[2][:4]), int(target[1]), int(target[0]))

	print('target: ', target_date)
	print('start: ', start_date)
	print('end: ', end_date)

	return target_date > start_date and target_date < end_date

# #Processes information
# def process(depart_range, depart_code, return_code):
# 	flight_list = deals[(depart_code,return_code)]
# 	for flight in flight_list:
# 		if is_in_date_range(flight)


if(__name__ == "__main__"):
	print("Hello World")
	print(is_in_date_range('12/1/1998 123', '12/12/2017 2123', '1/1/2000 123'))
	print(is_in_date_range('12/1/2010 123', '12/12/2017 2123', '1/1/2000 123'))

