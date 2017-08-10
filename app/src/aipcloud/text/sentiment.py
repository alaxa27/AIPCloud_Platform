# -*- coding: utf-8 -*-
# AIPCloud
#
# Author : Maxime Jumelle
# Date : 11/07/2017

import os
import numpy as np
import nltk
import pandas as pd
import gensim
import re
import time
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.models import model_from_json
import matplotlib.pyplot as plt

from aipcloud.text import word2vec
from aipcloud.statistics import regression

from ..exceptions import UnloadedException

class SentenceSentimentAnalyzer:

	MAX_LENGTH = 66
	TOP_WORDS = 40000

	def __init__(self):
		self.loaded = False
		self.model = None
	
	def load(self):
		print("Loading sentiment model.")
		json_file = open(os.path.join(os.path.dirname(__file__), "../data/FR_LSTM_model.json"), 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.model = model_from_json(loaded_model_json)
		self.model.load_weights(os.path.join(os.path.dirname(__file__), "../data/FR_LSTM_weights.h5"))
		self.W2V = word2vec.load(os.path.join(os.path.dirname(__file__), "../data/FR.vocab"))
		print("Sentiment model succesfully loaded.")
		self.loaded = True

	def analyze(self, text):
		if not(self.loaded):
			raise UnloadedException()
		
		text = text.lower()
		# We transform our sentence into word tokens
		tokens = nltk.word_tokenize(text)
		
		# Our input is a MAX_LENGTH integer vector
		vector = np.repeat(0, self.MAX_LENGTH)
		for i in range(min(self.MAX_LENGTH, len(tokens))):
			# If the word is in vocabulary
			if tokens[i] in self.W2V.wv.vocab:
				indexVal = self.W2V.wv.vocab[tokens[i]].index
				# If the word index was in the vocabulary during training phase
				if indexVal < self.TOP_WORDS:
					vector[i] = indexVal

		predict = self.model.predict(np.asarray([vector]))
		return predict[0]

class TextSentimentAnalyzer:

	TOP_WORDS = 40000

	def __init__(self):
		self.loaded = False
		self.analyzer = SentenceSentimentAnalyzer()
	
	def load(self):
		self.analyzer.load()
		self.loaded = True

	def analyze(self, text, verbose=False):
		if not(self.loaded):
			raise UnloadedException()

		eltime = time.time()
		
		text = text.lower()
		lines = re.split(r"[.;!?]+", text)

		classes = []
		weights = []
		lerp = []

		for line in lines:
			if len(line) > 3:
				an = self.analyzer.analyze(line)
				w = abs(an[2] - an[0]) + abs(an[1] - an[0]) + abs(an[2] - an[1])
				w /= 3
				classes.append(an)
				weights.append(w)
				lerp.append((an[2] + an[1]) / 2.0)

		N = len(classes)
		if N <= 1:
			print("At least two lines are needed.")
			return

		neg = [ classes[i][0] * weights[i] for i in range(N) ]
		mid = [ classes[i][1] * weights[i] for i in range(N) ]
		pos = [ classes[i][2] * weights[i] for i in range(N) ]

		sumWeight = sum(weights)
		distrib = [ sum(neg) / sumWeight, sum(mid) / sumWeight, sum(pos) / sumWeight ]
		accuracy = abs(distrib[0] - distrib[1]) + abs(distrib[2] - distrib[1])
		accuracy = accuracy**(1/3)
		mainLerp = distrib[2] - distrib[0]
		variance = sum([abs(lerp[i+1] - lerp[i]) for i in range(N - 1)]) / (N - 1)
		
		regModel = regression.SimpleLinearRegressionModel()
		regModel.fit(range(N), lerp)
		slope = regModel.parameters()[1] * N

		if verbose:
			eltime = time.time() - eltime
			print("Time to analyze : {:6.5f} second(s).".format(eltime))
			
			plt.plot(range(N), neg, color="r")
			plt.plot(range(N), mid, color="b")
			plt.plot(range(N), pos, color="g")
			plt.plot(range(N), np.repeat(distrib[0], N), color="r")
			plt.plot(range(N), np.repeat(distrib[1], N), color="b")
			plt.plot(range(N), np.repeat(distrib[2], N), color="g")
			plt.plot(range(N), lerp, color="black")
			plt.plot([0, N-1], regModel.predict([0, N-1]), color="m")
			plt.show()

		results = [ accuracy, slope, mainLerp, variance ]
		results = np.hstack((distrib, results))
		return results

	def summary(self, inputVector):
		distrib = inputVector[0:3]
		accuracy = inputVector[3]
		slope = inputVector[4]

		frenchClasses = [ "négatif", "neutre", "positif" ]	

		summary = "Le texte est "
		if accuracy >= 0.75:
			summary += frenchClasses[np.argmax(distrib)] + "."
		elif accuracy >= 0.5:
			summary += "plutôt neutre "
			argmin = np.argmin(distrib)
			if argmin == 1:
				summary += "avec des grandes variations positives et négatives."
			else:
				summary += frenchClasses[2 - argmin] + "."
		elif accuracy >= 0.35:
			summary += "semble être plutôt neutre "
			argmin = np.argmin(distrib)
			if argmin == 1:
				summary += "avec des grandes variations positives et négatives, "
			else:
				summary += frenchClasses[2 - argmin] + ", "
			summary += "mais l'analyse est moyennement pertinente."
		else:
			summary = "L'analyse n'est pas assez pertinente sur ce texte."

		if accuracy >= 0.35:
			if abs(slope) >= 0.4:
				if slope > 0:
					summary += " Le texte est négatif au début et positif vers la fin."
				else:
					summary += " Le texte est positif au début et négatif vers la fin."
			elif abs(slope) >= 0.12:
				argmin = np.argmin(distrib)
				if slope > 0:
					if argmin == 2:
						summary += " Le texte est neutre au début et positif vers la fin."
					elif argmin == 1:
						summary += " Le texte est négatif au début et neutre vers la fin."
				elif slope < 0:
					if argmin == 0:
						summary += " Le texte est neutre au début et négatif vers la fin."
					elif argmin == 1:
						summary += " Le texte est positif au début et neutre vers la fin."
			else:
				summary += " Le sentiment est constant tout au long du texte."
		return summary

class DialogueSentimentAnalyzer:

	def __init__(self):
		self.loaded = False
		self.analyzer = SentenceSentimentAnalyzer()

	def load(self):
		self.analyzer.load()
		self.loaded = True

	def analyze(self, listA, listB, verbose=False):
		if not(self.loaded):
			raise UnloadedException()
		if abs(len(listA) - len(listB)) >= 2:
			print("Input lists are not a dialogue.")
			return

		eltime = time.time()

		Na = len(listA)
		Nb = len(listB)
		N = max(Na, Nb)

		mainList = listA
		if Nb > Na:
			mainList = listB

		classesA = []
		classesB = []
		weightsA = []
		weightsB = []
		lerpA = []
		lerpB = []
		
		for i in range(N):
			if i < Na:
				anA = self.analyzer.analyze(listA[i])
				w = abs(anA[2] - anA[0]) + abs(anA[1] - anA[0]) + abs(anA[2] - anA[1])
				w /= 3
				weightsA.append(w)
				classesA.append(anA)
				print(str(w) + " - " + listA[i])
				print(anA)
				lerpA.append((anA[2] + anA[1]) / 3.0)
			if i < Nb:
				anB = self.analyzer.analyze(listB[i])
				w = abs(anB[2] - anB[0]) + abs(anB[1] - anB[0]) + abs(anB[2] - anB[1])
				w /= 3
				weightsB.append(w)
				classesB.append(anB)
				lerpB.append((anB[2] + anB[1]) / 3.0)

		negA = [ classesA[i][0] * weightsA[i] for i in range(Na) ]
		midA = [ classesA[i][1] * weightsA[i] for i in range(Na) ]
		posA = [ classesA[i][2] * weightsA[i] for i in range(Na) ]
		negB = [ classesB[i][0] * weightsB[i] for i in range(Nb) ]
		midB = [ classesB[i][1] * weightsB[i] for i in range(Nb) ]
		posB = [ classesB[i][2] * weightsB[i] for i in range(Nb) ]
		sumWeightsA = sum(weightsA)
		sumWeightsB = sum(weightsB)

		distribA = [ sum(negA) / sumWeightsA, sum(midA) / sumWeightsA, sum(posA) / sumWeightsA ]
		distribB = [ sum(negB) / sumWeightsB, sum(midB) / sumWeightsB, sum(posB) / sumWeightsB ]
		accuracyA = abs(distribA[0] - distribA[1]) + abs(distribA[2] - distribA[1])
		accuracyA = accuracyA**(1/3)
		accuracyB = abs(distribB[0] - distribB[1]) + abs(distribB[2] - distribB[1])
		accuracyB = accuracyB**(1/3)
		accuracy = (accuracyA + accuracyB) / 2.0

		regModel = regression.SimpleLinearRegressionModel()
		regModel.fit(range(Na), lerpA)
		slopeA = regModel.parameters()[1] * Na
		regModel.fit(range(Nb), lerpB)
		slopeB = regModel.parameters()[1] * Nb

		estimators = [ accuracyA, accuracyB, accuracy, slopeA, slopeB ]

		if verbose:
			eltime = time.time() - eltime
			print("Time to analyze : {:6.5f} second(s).".format(eltime))

		return distribA, distribB, estimators	

class CustomerServiceAnalyzer:

	MAX_LENGTH = 24
	TOP_WORDS = 50000

	def __init__(self):
		self.loaded = False
		self.sentimentAnalyzer = TextSentimentAnalyzer()
		self.agressAnalyzer = None
		self.refundAnalyzer = None

	def load(self):
		print("Loading customer service analyzer model.")

		# Loading agressivity network
		json_file = open(os.path.join(os.path.dirname(__file__), "../data/FR_LSTM_CS_Agres_model.json"), 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.agressAnalyzer = model_from_json(loaded_model_json)
		self.agressAnalyzer.load_weights(os.path.join(os.path.dirname(__file__), "../data/FR_LSTM_CS_Agres_weights.h5"))

		# Loading refund network
		json_file = open(os.path.join(os.path.dirname(__file__), "../data/FR_LSTM_CS_Refund_model.json"), 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.refundAnalyzer = model_from_json(loaded_model_json)
		self.refundAnalyzer.load_weights(os.path.join(os.path.dirname(__file__), "../data/FR_LSTM_CS_Refund_weights.h5"))

		self.W2V = word2vec.load(os.path.join(os.path.dirname(__file__), "../data/FR_CustomService.vocab"))
		self.sentimentAnalyzer.load()
		print("Customer service analyzer succesfully loaded.")
		self.loaded = True

	def analyze(self, text):
		if not(self.loaded):
			raise UnloadedException()
		sentiment = self.sentimentAnalyzer.analyze(text)
		satisf = -sentiment[0] + sentiment[2]

		text = text.lower()
		# We transform our sentence into word tokens
		tokens = nltk.word_tokenize(text)
		
		# Our input is a MAX_LENGTH integer vector
		vector = np.repeat(0, self.MAX_LENGTH)
		for i in range(min(self.MAX_LENGTH, len(tokens))):
			# If the word is in vocabulary
			if tokens[i] in self.W2V.wv.vocab:
				indexVal = self.W2V.wv.vocab[tokens[i]].index
				# If the word index was in the vocabulary during training phase
				if indexVal < self.TOP_WORDS:
					vector[i] = indexVal

		agress = self.agressAnalyzer.predict(np.asarray([vector]))[0][0]
		refund = self.refundAnalyzer.predict(np.asarray([vector]))[0][0]
		return [ satisf, agress, refund ]
		
