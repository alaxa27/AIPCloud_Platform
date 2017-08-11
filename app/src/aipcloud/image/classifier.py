# -*- coding: utf-8 -*-
# AIPCloud
#
# Author : Maxime Jumelle
# Date : 09/07/2017

from keras import applications
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.imagenet_utils import preprocess_input

from .utils import *
from ..exceptions import UnloadedException

class ImageClassifier:

	def __init__(self):
		self.name = ""
		self.loaded = False

	def isloaded(self):
		if not(self.loaded):
			raise UnloadedException()

class MultiLabelClassifier(ImageClassifier):

	def __init__(self):
		self.targetSize = (224, 224)

	def load(self):
		print("Loading the VGG16 model.")
		self.model = applications.VGG16(weights='imagenet', include_top=True)
		print("VGG16 model successfully loaded.")
		self.loaded = True

	def classify(self, inputImage, nbClasses=5, histogram=False):
		if nbClasses < 0:
			raise Exception("At least one class is needed for classification.")
		nbClasses = min(nbClasses, 1000)
		super(MultiLabelClassifier, self).isloaded()
		if type(inputImage) == str:
			image = ImageNetToArray(inputImage, targetSize=self.targetSize)
		else:
			image = inputImage
		preds = self.model.predict(image)
		if histogram:
			return preds
		return [ [ x[1], x[2] ] for x in decode_predictions(preds, top=nbClasses)[0] ]
