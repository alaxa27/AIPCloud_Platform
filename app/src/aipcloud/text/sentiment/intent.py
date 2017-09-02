import os, time
import numpy as np
import nltk
from keras.models import model_from_json

from ..word2vec import *
from ...exceptions import UnloadedException

class IntentAnalyzer:

	MAX_LENGTH = 24
	TOP_WORDS = 50000

	def __init__(self, analyzer=None):
		self.loaded = False
		if not(analyzer is None):
			self.loaded = True
		self.analyzer = analyzer

	def load(self):
		if self.loaded:
			return
		print("Loading intent analyzer model.")

		if self.analyzer is None:
			# Loading refund network
			json_file = open(os.path.join(os.path.dirname(__file__), "../../data/FR_LSTM_Intent_model.json"), 'r')
			loaded_model_json = json_file.read()
			json_file.close()
			self.analyzer = model_from_json(loaded_model_json)
			self.analyzer.load_weights(os.path.join(os.path.dirname(__file__), "../../data/FR_LSTM_Intent_weights.h5"))

			self.W2V = load(os.path.join(os.path.dirname(__file__), "../../data/FR_Intent.vocab"))

		print("Intent analyzer succesfully loaded.")
		self.loaded = True

	def analyze(self, text):
		if not(self.loaded):
			raise UnloadedException()
		execTime = time.time()

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

		prediction = self.analyzer.predict(np.asarray([vector]))[0]
		execTime = time.time() - execTime
		return {'res': prediction, 'exec_time': execTime}
