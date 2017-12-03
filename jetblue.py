import json
import datetime
import csv

#dollars is bool of if user wants to use dollars or not
def get_cheapest_flights(deals_list, dollars):
	cheapest_flights =[]
	sorted_list = sorted(deals_list, key = lambda flight: flight[6])
	min_price = min(deals_list, key = lambda flight: flight[6])[6]
	for flight in sorted_list:
		if flight[6] == min_price:
			cheapest_flights.append(flight)
		else:
			break
	print(cheapest_flights)
	print("DONE")
	if dollars:
		return list(filter(lambda flight: flight[5] == 'LOWEST', cheapest_flights))
	else:
		return list(filter(lambda flight: flight[5] != 'LOWEST', cheapest_flights))
	
#TODO: This is the same as get_cheapest_flight
def getLowestPrice(data_tuple):
	data = data_tuple[1]
	min_price = 99999
	for flight in data:
		if flight[5] <= min_price:
			min_row = flight
			min_price = flight[5]
	return min_row

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

	if target.find('/') != -1:
		uses_slashes = True
	elif target.find('-') != -1:
		uses_dashes = True

	if uses_dashes:
		target = target.split('-')
		target_date = datetime.date(int(target[0]), int(target[1]), int(target[2][:2]))
		#print(target)
	elif uses_slashes: 
		target = target.split('/')
		target_date = datetime.date(int(target[2][:4]), int(target[0]), int(target[1]))
		
	start = start.split("/")
	
	end = end.split("/")
	
	start_date = datetime.date(int(start[2]), int(start[0]), int(start[1]))
	end_date = datetime.date(int(end[2]), int(end[0]), int(end[1]))

	return target_date > start_date and target_date < end_date

#Processes information
#Assumes start_date and end_date in form of 'mm/dd/yyyy'
def process(deals, low_fares, left_date, right_date, depart_code, dest_code):
	deals_in_range = []
	lowest_fares_in_range = []
	deal_list = deals[(depart_code,dest_code)]
	low_list = low_fares[(depart_code, dest_code)]
	for flight in deal_list:
		if is_in_date_range(left_date, right_date, flight[3]):
			deals_in_range.append(flight)

	for flight in low_list:
		if is_in_date_range(left_date, right_date, flight[2]):
			lowest_fares_in_range.append(flight)

	return (deals_in_range, lowest_fares_in_range)

if(__name__ == "__main__"):
	print("Hello World")
	# print(is_in_date_range('12/01/1998', '12/12/2017', '01/01/2000'))
	# print(is_in_date_range('12/01/2010', '12/12/2017', '01/01/2000'))
