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
#import matplotlib.pyplot as plt


from . import word2vec

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

		text = text.decode('utf8').lower()
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

	MAX_LENGTH = 66
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

		for line in lines:
			if len(line) > 10:
				an = self.analyzer.analyze(line)
				w = abs(an[2] - an[0]) + abs(an[1] - an[0]) + abs(an[2] - an[1])
				w /= 3
				classes.append(an)
				weights.append(w)

		neg = [ classes[i][0] * weights[i] for i in range(len(classes)) ]
		mid = [ classes[i][1] * weights[i] for i in range(len(classes)) ]
		pos = [ classes[i][2] * weights[i] for i in range(len(classes)) ]
		N = len(classes)
		sumWeight = sum(weights)
		distrib = [ sum(neg) / sumWeight, sum(mid) / sumWeight, sum(pos) / sumWeight ]
		accuracy = abs(distrib[0] - distrib[1]) + abs(distrib[2] - distrib[1])
		accuracy = accuracy**(1/3)

		if verbose:
			eltime = time.time() - eltime
			print("Time to analyze : {:6.5f} second(s).".format(eltime))

			plt.plot(range(N), neg, color="r")
			plt.plot(range(N), mid, color="b")
			plt.plot(range(N), pos, color="g")
			plt.plot(range(N), np.repeat(distrib[0], N), color="r")
			plt.plot(range(N), np.repeat(distrib[1], N), color="b")
			plt.plot(range(N), np.repeat(distrib[2], N), color="g")
			plt.show()

		results = [ accuracy ]
		results = np.hstack((distrib, results))
		return results

class CustomerServiceAnalyzer:

	MAX_LENGTH = 24
	TOP_WORDS = 50000

	def __init__(self):
		self.loaded = False
		self.sentimentAnalyzer = SentenceSentimentAnalyzer()
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
