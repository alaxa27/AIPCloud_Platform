import os, time
import numpy as np
import nltk
from keras.models import model_from_json

from ..word2vec import *
from ...exceptions import UnloadedException

class SentenceSentimentAnalyzer:

	MAX_LENGTH = 66
	TOP_WORDS = 40000

	def __init__(self):
		self.loaded = False
		self.model = None

	def load(self):
		print("Loading sentiment model.")
		json_file = open(os.path.join(os.sep, "data/FR_LSTM_model.json"), 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.model = model_from_json(loaded_model_json)
		self.model.load_weights(os.path.join(os.sep, "data/FR_LSTM_weights.h5"))
		self.W2V = load(os.path.join(os.sep, "data/FR.vocab"))
		print("Sentiment model succesfully loaded.")
		self.loaded = True

	def analyze(self, text):
		execTime = time.time()
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
		execTime = time.time() - execTime
		return {'res': predict[0], 'exec_time': execTime}
