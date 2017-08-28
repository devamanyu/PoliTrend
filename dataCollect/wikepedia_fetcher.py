import numpy as np, pandas as pd
import os
import urllib2, urllib
import json
from pprint import pprint
import re
from bs4 import BeautifulSoup
import datetime as DT
import dateutil.parser
import csv

def main(name=None):

	path = '../app/data/'+name

	file = open(path+'.csv','w')
	wr = csv.writer(file, quoting=csv.QUOTE_ALL)

	# Wikipedia API to collect all revisions of a political entity page
	response = urllib2.urlopen('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=revid|ids|timestamp&rvlimit=max&format=json&titles='+name)
	json_response = json.load(response)
	keyid = json_response['query']['pages'].keys()[0]
	length = len(json_response['query']['pages'][keyid]['revisions'])
	revision_ids = [json_response['query']['pages'][keyid]['revisions'][ind]['revid'] for ind in range(length) ]
	timestamps = [json_response['query']['pages'][keyid]['revisions'][ind]['timestamp'] for ind in range(length) ]
	

	# yourdate = dateutil.parser.parse(timestamps[0]) #Alternative Datetime parser: dateutil
	dates =  [DT.datetime.strptime(timestamps[i], '%Y-%m-%dT%H:%M:%SZ') for i in range(len(timestamps))]


	for ind, ids in enumerate(revision_ids):
		tupl=[]
		tupl.append(dates[ind])

		query_text = 'https://en.wikipedia.org/w/api.php?action=parse&format=json&oldid='+str(ids)
		response = urllib2.urlopen(query_text)
		json_response = json.load(response)
		html_content = json_response["parse"]["text"]['*']
		soup = BeautifulSoup(html_content, "html5lib")
		article = soup.find("div", {"class":"mw-parser-output"}).findAll('p')
		wiki_text = ''
		for element in article:
			wiki_text += ''.join(element.findAll(text = True)).encode('utf-8')+'\n'
		tupl.append(wiki_text)
		wr.writerow(tupl)


if __name__ == '__main__':

	names = np.array(pd.read_csv('./input/political_parties.csv', header=None))
	names = [urllib.quote(names[i][0]) for i in xrange(len(names))]

	for name in names:
		print name
		main(name)
		