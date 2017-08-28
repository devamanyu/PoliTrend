import numpy as np, pandas as pd, keras, gensim
from doc2vec import *
from keras.layers.core import *
from keras.layers.recurrent import LSTM
from keras.models import *
from keras import backend as K
from keras.activations import softmax

NAME = "glassdoor_reviews" # input dataset
TRAIN_DOC2VEC = False # flag to retrain doc2vec 

def loadData():
	'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	'' Loads the dataset and gets document embeddings, also labels ''
	'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	if TRAIN_DOC2VEC:
		trainDoc2Vec(NAME)
	model = gensim.models.Doc2Vec.load('./models/doc2vec.model')
	data = np.asarray(pd.read_csv("./input/"+NAME+".csv", header=None))
	docs = [data[i][1] for i in xrange(data.shape[0])] + [data[i][2] for i in xrange(data.shape[0])] 
	docLabels = [ NAME+"_"+str(i) for i in xrange(2*data.shape[0])]
	docEmbeddings = np.asarray([model.docvecs[docLabels[i]] for i in xrange(len(docs))], dtype=K.floatx())
	labels = np.asarray([[1] for _ in xrange(data.shape[0])] + [[0] for _ in xrange(data.shape[0])])
	return (docEmbeddings, labels)



def trainModel():

	data, labels = loadData()
	DIM = data.shape[1]

	# Training a keras model
	inputs = Input(shape=(DIM,))
	dense_out = Dense(1000, activation='tanh')(inputs)
	dropout = Dropout(0.9)(dense_out)
	output = Dense(1, activation='sigmoid')(dropout)
	print output._keras_shape

	model = Model(inputs, output)
	model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	print(model.summary())

	model.fit(data, labels, epochs=200, batch_size=64, validation_split=0.1)
	model.save("./models/classifier.h5")


if __name__ == '__main__':

	trainModel()



