import numpy as np
import pandas
import random
import sys
'''class Instance():
	def __init__(self):
		self.
'''
class Attribute():
	'''
	dtype = data type
	vals = None if real, possible nominal-values otherwise
	column = the actual column values for this data set
	'''
	def __init__(self):
		self.name = None
		self.dtype = None 
		self.vals = None
		self.column = None

	def initFromArff(self, line, col):
		tokens = line.split()
		print tokens
		self.name = tokens[1].strip()	
		if 'NUMERIC' not in tokens[2].upper() and 'REAL' not in tokens[2].upper():
			self.vals = tokens[2][1:-1].split(',')
			self.dtype = 'nominal'
		else:
			self.dtype = 'real'
		self.column = col
class Dataset():
	def __init__(self):
		'''
		instances = an ordered list of instances
		features =  column subset of instances that form the features
		labels = column subet of instnaces that form the labels
		name = name of data set
		attributes = attribute objects, contain information about each column
		'''
		self.instances = None
		self.features = None
		self.labels = None
		self.name = None
		self.attributes = None
		self.numLabels = None
		self.colsAtStart = True
		self.featureStart = None
		self.featureEnd = None
		self.labelStart= None
		self.labelEnd = None

	def loadArff(self, file_name):
		print 'file name!'
		print file_name
		lines = None
		#with open(file_name) as f:
			#lines = f.readlines()
		lines = [line.rstrip('\n') for line in open(file_name)]
		print lines
		isMetaData = True
		line = 0
		self.attributes = []
		column = 0
		print 'before'
		while(isMetaData):
			if '@RELATION' in lines[line].upper():
				tokens = lines[line].split(' ')
				self.name = tokens[1][1:-2]	
				self.numLabels = int(tokens[3].strip()[0:-1])
				if self.numLabels < 0:
					self.colsAtStart = False		
				self.numLabels = abs(self.numLabels)
			elif '@ATTRIBUTE' in lines[line].upper():
				a = Attribute()	
				a.initFromArff(lines[line], column)
				column = column + 1
				self.attributes.append(a)
			elif '@DATA' in lines[line].upper():
				isMetaData = False
			line = line + 1
		print 'after'
		if self.colsAtStart:
			self.labels = self.attributes[0:self.numLabels]
			self.features = self.attributes[self.numLabels:]
			self.featureStart = self.numLabels
			self.featureEnd = len(self.attributes)
			self.labelStart = 0
			self.labelEnd = self.numLabels
		else:
			self.labels = self.attributes[-1*self.numLabels:]
			self.features = self.attributes[0:-1*self.numLabels]
			self.featureStart = 0
			self.featureEnd = len(self.attributes) - self.numLabels
			self.labelStart = len(self.attributes) - self.numLabels
			self.labelEnd = len(self.attributes)
		self.instances = []
		print 'here'
		print line
		print len(lines)
		while line < len(lines):
			print lines[line]
			if not lines[line].isspace() and '%' not in lines[line] and not lines[line].strip() == '':
				self.instances.append(lines[line].split(','))
			line = line + 1

		
		self.instances = np.asarray(self.instances) # this will convert everything to strings (possibly)
		print 'len attributes'
		print len(self.attributes)
		for i in range(0,len(self.attributes)):
			print self.attributes[i].dtype
			if self.attributes[i].dtype == 'nominal':
				print self.instances.shape
				arr = self.instances[:,i]				
				u, indices = np.unique(arr, return_inverse=True)
				self.instances[:,i] = indices 
		self.instances = np.asarray(self.instances, dtype='float')
		
	def shuffle(self):
		random.shuffle(self.instances)

	def getFeatures(self):
		return self.instances[:,self.featureStart:self.featureEnd]
	def getLabels(self):
		return self.instances[:,self.labelStart:self.labelEnd]

	def convertToDummy(self, labelCols):
		cols = []
		for i in range(0,len(labelCols[0])):
			b = pandas.get_dummies(labelCols[:,i])
			cols.append(b.values)
			
		result = []
		for row in range(0,len(labelCols)):
			curr = []
			for c in range(0,len(labelCols[0])):
				curr.append(cols[c][row])
			result.append(curr)
		result = np.asarray(result)
		return result

			
	def printInfo(self):
		print 'num labels'
		print self.numLabels
		print 'numFeatures'
		print len(self.features)
		print 'label types'
		for i in self.labels:
			print i.name
			print i.dtype
		for i in self.features:
			print i.name
			print i.dtype
		
				
			
print 'hi'
#d = Dataset()
#d.loadArff('music.arff')
#printInfo()
