import os, time
import numpy as np
import nltk
from keras.models import model_from_json

from .text import TextSentimentAnalyzer
from ..word2vec import *
from ...exceptions import UnloadedException

class CustomerServiceAnalyzer:

	MAX_LENGTH = 24
	TOP_WORDS = 50000

	def __init__(self, sentimentAnalyzer=None):
		self.loaded = False
		self.sentimentAnalyzer = sentimentAnalyzer
		self.agressAnalyzer = None
		self.refundAnalyzer = None

	def load(self):
		print("Loading customer service analyzer model.")

		# Loading agressivity network
		json_file = open(os.path.join(os.path.dirname(__file__), "../../data/FR_LSTM_CS_Agres_model.json"), 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.agressAnalyzer = model_from_json(loaded_model_json)
		self.agressAnalyzer.load_weights(os.path.join(os.path.dirname(__file__), "../../data/FR_LSTM_CS_Agres_weights.h5"))

		# Loading refund network
		json_file = open(os.path.join(os.path.dirname(__file__), "../../data/FR_LSTM_CS_Refund_model.json"), 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.refundAnalyzer = model_from_json(loaded_model_json)
		self.refundAnalyzer.load_weights(os.path.join(os.path.dirname(__file__), "../../data/FR_LSTM_CS_Refund_weights.h5"))

		self.W2V = load(os.path.join(os.path.dirname(__file__), "../../data/FR_CustomService.vocab"))
		if self.sentimentAnalyzer is None:
			self.sentimentAnalyzer = TextSentimentAnalyzer()
			self.sentimentAnalyzer.load()
		print("Customer service analyzer succesfully loaded.")
		self.loaded = True

	def analyze(self, text):
		if not(self.loaded):
			raise UnloadedException()
		execTime = time.time()
		results = self.sentimentAnalyzer.analyze(text)
		sentiment = results["res"]
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
		execTime = time.time() - execTime
		return {'res': [ satisf, agress, refund ], 'exec_time': execTime}
