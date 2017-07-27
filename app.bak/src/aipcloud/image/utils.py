# -*- coding: utf-8 -*-
# AIPCloud
#
# Author : Maxime Jumelle
# Date : 09/07/2017

import os
import cv2
import numpy as np
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image

def ImageNetToArray(filePath, targetSize):
	if not(os.path.exists(filePath)):
		raise Exception("The file " + filePath + " was not found.")
	img = image.load_img(filePath, target_size=targetSize)
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	x = preprocess_input(x)
	return x

def LoadImage(filePath):
	if not(os.path.exists(filePath)):
		raise Exception("The file " + filePath + " was not found.")
	return cv2.imread(filePath, cv2.IMREAD_COLOR)
