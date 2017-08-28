from flask import Flask, render_template, Response, request, redirect, url_for
import json
from os import listdir
from os.path import isfile, join
import urllib
from predictSentiment import predict
from bson import json_util
import json
import numpy as np


app = Flask(__name__)

@app.route("/")
def main():
	''' 
	''''''''''''''''''''''''''''''''''''''
	 Rendering the landing page
	''''''''''''''''''''''''''''''''''''''
	'''
    return render_template('index.html')

@app.route('/getName', methods=['POST'])
def getName():
	''' 
	''''''''''''''''''''''''''''''''''''''
	 Returns the name of political entities
	''''''''''''''''''''''''''''''''''''''
	'''
	mypath = "./data/"
	onlyfiles = [urllib.unquote(f[:-4]) for f in listdir(mypath) if isfile(join(mypath, f))]
	return json.dumps(onlyfiles);


@app.route('/getSentiment', methods=['POST'])
def getSentiment():
	''' 
	''''''''''''''''''''''''''''''''''''''''''''''''
	 Predicts the sentiment of the wikipedia history
	''''''''''''''''''''''''''''''''''''''''''''''''
	'''
	jsondata = request.json
	dates, predictions, name = predict(jsondata)
	return json.dumps(name)

if __name__ == "__main__":
	app.run()
