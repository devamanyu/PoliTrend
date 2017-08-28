import numpy as np, pandas as pd, keras, gensim
from keras.layers.core import *
from keras.layers.recurrent import LSTM
from keras.models import *
from keras import backend as K
from keras.activations import softmax
from keras.models import load_model
import gensim
import datetime as DT
import matplotlib.pyplot as plt
import matplotlib
import urllib

def predict(name=None):
	
	name = urllib.quote(name)
	print name
	assert(name!= None)

	model = load_model("../train/models/classifier.h5")
	doc2vec = gensim.models.Doc2Vec.load('../train/models/doc2vec.model')

	data = np.asarray(pd.read_csv('./data/'+name+'.csv', header=None))
	DIM = 300

	predictions = np.asarray([model.predict(doc2vec.infer_vector(data[i][1].split()).reshape(1,DIM)).squeeze() for i in xrange(data.shape[0])])
	time = data[:,0]

	dates =  [DT.datetime.strptime(time[i], '%Y-%m-%d %H:%M:%S') for i in range(len(time))]


	dates = matplotlib.dates.date2num(dates)
	plt.plot(dates, predictions)
	plt.show()

# if __name__ == '__main__':

# 	name = 'Aam%20Aadmi%20Party'
# 	predict(name)