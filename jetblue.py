import json
import datetime
import csv

def getAirportData(airport_data, name):
	return airport_data[name]

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

		start_date = datetime.date(int(start[2][:4]), int(start[0]), int(start[1]))
		end_date = datetime.date(int(end[2][:4]), int(end[0]), int(end[1]))
		target_date = datetime.date(int(target[2][:4]), int(target[0]), int(target[1]))

	print('target: ', target_date)
	print('start: ', start_date)
	print('end: ', end_date)

	return target_date > start_date and target_date < end_date

# #Processes information
#Assumes start_date and end_date in form of 'mm/dd/yyyy'
def process(start_date, end_date, depart_code, dest_code):
	left_date = start_date.split('/')
	right_date = end_date.split('/')
	left_date = datetime.date(left_date[2], left_date[0], left_date[1])
	right_date = datetime.date(right_date[2], right_date[0], right_date[1])

	flight_list = deals[(depart_code,dest_code)]
	flights_in_range = []
	for flight in flight_list:
		if is_in_date_range(left_date, right_date, flight[2]):
			flights_in_range.append(flight)

	return flights_in_range

if(__name__ == "__main__"):
	print("Hello World")
	print(is_in_date_range('12/1/1998 123', '12/12/2017 2123', '1/1/2000 123'))
	print(is_in_date_range('12/1/2010 123', '12/12/2017 2123', '1/1/2000 123'))