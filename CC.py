import random
import pandas
from NNet import NNet
import numpy as np

class CC():
	'''
	Chain Classifier
	Keeps track of chain ordering. Always returns predictions in form 0,1,2... (rather than the random prediction order)
	'''
	
	def __init__(self,  numL):
		self.numLabels = numL
		self.chainOrder = range(0,self.numLabels)
		random.shuffle(self.chainOrder)
		self.models = []

	def train(self, features, labels, convertLabels=False):
		# labels to one-hot
		for i in self.chainOrder:
			currLabels = labels[:,i]
			if convertLabels:
				b = pandas.get_dummies(currLabels)
				currLabels = b.values
				#currLabels = b.values.tolist()
			n = NNet()
			n.train(features,currLabels, None)
			self.models.append(n)
			#add labels to features
			col = np.asarray(currLabels)
			features = np.concatenate((features,col), axis=1)
			#features = np.concatenate((features, col.T), axis=1)
		
	def predict(self, features):
		prediction = []
		for m in self.models:
			pred = m.predict(features)
			prediction.append(pred.tolist())
			col = np.asarray(pred)
			#features = np.concatenate((features,col), axis=1)
			features = np.append(features,col)
		#reorder predictions according to chain order. i.e. chaing 4,3,2,5,1 back to 1,2,3,4,5
		orderedPrediction = []
		for i in self.chainOrder:
			orderedPrediction.append(prediction[self.chainOrder[i]])
		#return prediction # this is a python list
		return orderedPrediction # this is a python list
	
	def predictAll(self, featureRows):
		predictions = []
		for f in featureRows:
			predictions.append(self.predict(f))	
		print 'chekc here!'
		return np.asarray(predictions)

		







				
			
		
			
		
			
		
		
