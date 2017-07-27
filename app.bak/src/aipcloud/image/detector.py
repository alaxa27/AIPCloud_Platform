# -*- coding: utf-8 -*-
# AIPCloud
#
# Author : Maxime Jumelle
# Date : 10/07/2017

import os
import numpy as np
import cv2

from aipcloud.image import utils

class ImageDetector:

	def __init__(self):
		self.name = ""

class FaceDetector(ImageDetector):

	def load(self):
		self.eyeCascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), "../data/haarcascade_eye.xml"))
		self.faceCascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), "../data/haarcascade_face.xml"))

	def detect(self, inputImage, detectEyes=False):
		image = inputImage
		if type(inputImage) == str:
			image = utils.LoadImage(inputImage)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(25, 25))
		if detectEyes:
			facesEyes = []
			index = 0
			for (x, y, w, h) in faces:
				eyes = self.eyeCascade.detectMultiScale(gray[y:y+h, x:x+w])
				facesEyes.append([ faces[index], eyes ])
				index += 1
			return facesEyes
		return faces
