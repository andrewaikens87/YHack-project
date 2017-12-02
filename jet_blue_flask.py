from flask import Flask
from flask import jsonify
from flask import request
import json
import time
import jetblue as jb

app = Flask(__name__)
current_date = time.gmtime() #TODO: Double check this gets the right time
current_year = current_date[-4]


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
	app.run()