# -*- coding: utf-8 -*-
# AIPCloud
#
# Author : Maxime Jumelle
# Date : 11/07/2017

import os
import gensim
import numpy as np
import gensim, logging
from gensim.models import word2vec

def save(tokens, filename, size=100):
	vocab = []
	for i in xrange(len(tokens)):
		for j in xrange(len(tokens[i])):
			vocab.append(tokens[i][j])
	model = word2vec.Word2Vec(vocab, size=size, min_count=3, window=5, workers=2)
	model.save(filename)
	return model

def load(filename):
	return word2vec.Word2Vec.load(filename)
