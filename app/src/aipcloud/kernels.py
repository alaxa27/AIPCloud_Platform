# AIPCloud
#
# Author : Maxime Jumelle
# Date : 06/07/2017

import numpy as np
import math

def LinearKernel(x, y):
	return np.dot(x, y)

def PolynomialKernel(x, y, deg=2, alpha=1, beta=0):
	return (alpha * np.dot(x, y) + beta)**deg

def RBFKernel(x, y, alpha=1):
	return math.exp(-alpha * np.linalg.norm(x - y)**2)
	
def TanhKernel(x, y, alpha=1, beta=0):
	return math.tanh(alpha * np.dot(x, y) + beta)

def SigmoidKernel(x, y, alpha=1):
	return 1.0 / (1.0 + np.exp(-alpha * x))

def GetKernelParameter(kernel):
	if kernel == 'linear':
		return LinearKernel
	elif kernel == 'polynomial':
		return PolynomialKernel
	elif kernel == 'rbf':
		return RBFKernel
	elif kernel == 'tanh':
		return TanhKernel
	elif kernel == 'sigmoid':
		return SigmoidKernel
	else:
		return kernel
