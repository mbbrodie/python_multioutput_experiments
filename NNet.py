import numpy as np
import pandas
import math
import sys

class NNet():
	'''Single hidden layer Neural Network with sigmoidal outputs'''
	def __init__(self):
		self.hWeights = None
		self.oWeights = None
		self.lr = .01

	def train(self, features, labels, stopCriteria, numHidden=None, convertLabels=False):
		if convertLabels: 
                	b = pandas.get_dummies(labels[:,0])
                	labels = b.values
		#labels of form [0,0,1] or [.23,-.35,.44]
		mu, sigma = 0, 0.1 # mean and standard deviation
		if numHidden == None:
			numHidden = len(features[0]) * 2
		self.hWeights = np.random.normal(mu, sigma, (numHidden, len(features[0])+1))
		self.oWeights = np.random.normal(mu, sigma, (len(labels[0]), numHidden + 1)) # the plus one is for bias
		b = np.ones(len(features))
		features = np.concatenate((features,np.asarray([b]).T), axis=1)
		#train
		improving = True
		epoch = 0
		while improving:
			for f in range(0,len(features)):
				hFeat = self.doActivation('sigmoid', np.dot(self.hWeights,features[f].T)) # check here for error
				hFeat = np.concatenate((hFeat,np.asarray([1])),axis=0)	
				oAct = self.doActivation('sigmoid', np.dot(self.oWeights, hFeat))
				#calc error and gradient
				err = (labels[f] - oAct) * oAct * (np.ones(len(oAct)) - oAct)
				#oUpdate =  np.outer(err.T,hFeat) * self.lr
				oUpdate =  np.outer(err,hFeat) * self.lr
				hFeat = hFeat[0:-1]
				temp_oWeights = self.oWeights[:,0:-1]
				hErr = hFeat * (np.ones(len(hFeat)) - hFeat) * np.dot(err,temp_oWeights)
				hUpdate = np.outer(hErr.T,features[f]) * self.lr
				self.oWeights = self.oWeights + oUpdate
				self.hWeights = self.hWeights + hUpdate
			
			#check if improving
			epoch = epoch + 1			
			if epoch > 10:
				improving = False	
			
			#hFeat = np.concatenate((hFeat,np.asarray([b]).T), axis=1)

	def doActivation(self, name, vals):
		if name == 'sigmoid':
			return self.sigmoid(vals)

	def sigmoid(self, X):
		'''Compute the sigmoid function '''
		den = 1.0 + math.e ** (-1.0 * X)
		d = 1.0 / den
		return d

	def predict(self, features):
		#labels of form [0,0,1] or [.23,-.35,.44]
		features = np.concatenate((features,np.asarray([1])), axis=0)
		hFeat = self.doActivation('sigmoid', np.dot(self.hWeights,features)) # check here for error
		hFeat = np.concatenate((hFeat,np.asarray([1])),axis=0)
		oAct = self.doActivation('sigmoid', np.dot(self.oWeights, hFeat))
		return oAct
