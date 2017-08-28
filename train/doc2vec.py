import pandas as pd
import numpy as np
import gensim
TaggedDocument = gensim.models.doc2vec.TaggedDocument


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield TaggedDocument(doc.split(), [self.labels_list[idx]])


def trainDoc2Vec(dataset=None):
	''' 
	'''''''''''''''''''''''''''''''''''''''''''''''''
	Doc2Vec training funciton, trained model is saved
	'''''''''''''''''''''''''''''''''''''''''''''''''
	'''
	assert(dataset != None)
	
	data = np.asarray(pd.read_csv("./input/"+dataset+".csv", header=None))
	
	docLabels = [ dataset+"_"+str(i) for i in xrange(2*data.shape[0])]
	docs = [data[i][1] for i in xrange(data.shape[0])] + [data[i][2] for i in xrange(data.shape[0])] 

	it = LabeledLineSentence(docs, docLabels)
	model = gensim.models.Doc2Vec(size = 300, window=10, min_count=5, workers=11, alpha=0.025 , min_alpha=0.025 )
	model.build_vocab(it)

	for epoch in range(100):
		print epoch
		model.alpha -= 0.002
		model.min_alpha = model.alpha
		model.train(it, total_examples=model.corpus_count, epochs=model.iter)
		model.save("./models/doc2vec.model")

