# -*- coding: utf-8 -*-
# AIPCloud
#
# Author : Maxime Jumelle
# Date : 30/07/2017

import os, string, itertools, operator
import math
import numpy as np
import nltk
import pandas as pd
import gensim
import time

from ..exceptions import UnloadedException

class KeywordExtraction():

	def __init__(self):
		self.loaded = False

	def load(self):
		with open(os.path.join(os.path.dirname(__file__), "../data/fr_stopwords.txt"), 'r') as f:
			content = f.readlines()
		content = [x.strip() for x in content]

		self.stopwords = set.union(set(nltk.corpus.stopwords.words('french')), set(content))
		self.punctuation = set.union(set(string.punctuation), set({"«", "»", "“", "”", "‘", "’", "'"}))

		self.loaded = True

	def extract(self, text, keywordCount=6, verbose=False):
		if not(self.loaded):
			raise UnloadedException()
		execTime = time.time()

		scores = self.score_keyphrases_by_textrank(text, n_keywords=keywordCount)
		# We want to know if there is capital letters in the original word or chunk
		for i in range(len(scores)):
			word = scores[i][0]
			index = text.lower().find(word)
			scores[i] = (text[index:(index+len(word))], scores[i][1])

		if verbose:
			print("Time to extract keywords : {:6.5f} second(s).".format(execTime))

		execTime = time.time() - execTime
		return {'res': scores, 'exec_time': execTime}

	def extract_candidate_words(self, text, good_tags=set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])):
		# Tokenization of each word in each sentence
		tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)))
		return [word.lower() for word, tag in tagged_words if tag in good_tags and word.lower() not in self.stopwords and len(word) >= 3 and not all(char in self.punctuation for char in word)]

	def score_keyphrases_by_textrank(self, text, n_keywords=10):
		from itertools import takewhile, tee
		import networkx

		# We tokenize each word of each sentence
		words = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
		# We get the potential candidates
		candidates = self.extract_candidate_words(text)
		# We build the graph-based ranking
		graph = networkx.Graph()
		graph.add_nodes_from(set(candidates))
		# Iteration over word-pairs, add unweighted edges into graph
		def pairwise(iterable):
			"""s -> (s0,s1), (s1,s2), (s2, s3), ..."""
			a, b = tee(iterable)
			next(b, None)
			return zip(a, b)
		for w1, w2 in pairwise(candidates):
			if w2:
				graph.add_edge(*sorted([w1, w2]))
		# Score nodes using default pagerank algorithm, sort by score, keep top n_keywords
		ranks = networkx.pagerank(graph)
		if 0 < n_keywords < 1:
			n_keywords = int(round(len(candidates) * n_keywords))

		word_ranks = {word_rank[0]: word_rank[1]
		  for word_rank in sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:n_keywords]}
		keywords = set(word_ranks.keys())
		# Merge keywords into keyphrases
		keyphrases = {}
		j = 0
		for i, word in enumerate(words):
			if i < j:
				continue
			if word in keywords:
				kp_words = list(takewhile(lambda x: x in keywords, words[i:i+10]))
				avg_pagerank = sum(word_ranks[w] for w in kp_words) / float(len(kp_words))
				keyphrases[' '.join(kp_words)] = avg_pagerank
				j = i + len(kp_words)

		return sorted(keyphrases.items(), key=lambda x: x[1], reverse=True)
