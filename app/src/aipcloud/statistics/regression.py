# -*- coding: utf-8 -*-
# AIPCloud
#
# Author : Maxime Jumelle
# Date : 03/07/2017

import numpy as np
import math

from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
import sklearn.gaussian_process.kernels as GPKernels

from ..exceptions import UnfittedException
from ..kernels import GetKernelParameter

class Model:

	def __init__(self):
		self.fitted = False

	def fit(self, x, y):
		raise Exception('The fit function of the regression model is not defined.')

	def isfit(self):
		if not(self.fitted):
			raise UnfittedException()

# A simple linear regression over 1-D value
class SimpleLinearRegressionModel(Model):

	name = "Simple Linear Regression"

	def __init__(self):
		Model.__init__(self)
		self.beta0 = 0
		self.beta1 = 0
		self.R2 = 0

	def fit(self, X, Y, verbose=False):
		n = len(X)
		mx = sum(X) / len(X)
		my = sum(Y) / len(Y)
		cov = (1 / n) * sum((X - np.repeat(mx, n)) * (Y - np.repeat(my, n)))
		varx = (1 / n) * sum((X - np.repeat(mx, n))**2)
		vary = (1 / n) * sum((Y - np.repeat(my, n))**2)

		# Estimators of parameters
		self.beta1 = cov / varx
		self.beta0 = my - mx * self.beta1

		# Accuracy estimators
		self.R2 = (cov / (math.sqrt(varx * vary)))**2

		self.fitted = True

		if verbose:
			print("Parameters of " + self.name + " :")
			print("-" * 30)
			print("Beta 0 \t" + str(self.beta0))
			print("Beta 1 \t" + str(self.beta1))
			print("-" * 30)
			print("Accuracy of " + self.name + " :")
			print("-" * 30)
			print("R-squared \t" + str(self.R2))
			print("-" * 30)

	def predict(self, X):
		super(SimpleLinearRegressionModel, self).isfit()
		return [ self.beta0 + self.beta1 * X[k] for k in range(len(X)) ]

	def parameters(self):
		super(SimpleLinearRegressionModel, self).isfit()
		return [ self.beta0, self.beta1 ]

	def accuracy(self):
		return [ self.R2 ]

# A multiple linear regression over n-D value
class MultiLinearRegressionModel(Model):

	name = "Multiple Linear Regression"

	def __init__(self):
		Model.__init__(self)
		self.beta = []
		self.R2 = 0
		self.R2a = 0

	def fit(self, X, Y, verbose=False):
		X = np.array(X)
		n = len(X)
		p = X.shape[1]
		Xin = np.hstack([ np.ones([n, 1]), X ])

		# Estimators of parameters
		self.beta = np.linalg.solve(np.dot(np.transpose(Xin), Xin), np.dot(np.transpose(Xin), Y))
		my = sum(Y) / n

		# Accuracy estimators
		self.SCR = sum((Y - np.dot(Xin, np.transpose(self.beta)))**2)
		self.SST = sum((Y - np.repeat(my, n))**2)
		residue = self.SCR / self.SST
		self.R2 = 1.0 - residue
		self.R2a = 1.0 - (n / (n - p)) * residue

		self.fitted = True

		if verbose:
			print("Accuracy of " + self.name + " :")
			print("-" * 30)
			print("Multiple R-squared \t" + str(self.R2))
			print("Adjusted R-squared \t" + str(self.R2a))
			print("-" * 30)

	def predict(self, X):
		super(MultiLinearRegressionModel, self).isfit()
		return [ self.beta[0] + np.dot(X[k], self.beta[1:]) for k in range(len(X)) ]

	def parameters(self):
		super(MultiLinearRegressionModel, self).isfit()
		return self.beta

	def accuracy(self):
		super(MultiLinearRegressionModel, self).isfit()
		return [ self.R2, self.R2a ]

# A ridge linear regression over n-D value
class RidgeRegressionModel(Model):

	name = "Ridge Linear Regression"

	def __init__(self):
		Model.__init__(self)
		self.beta = []
		self.R2 = 0
		self.aR2 = 0

	def fit(self, X, Y, alpha=1, verbose=False):
		if alpha < 0:
			raise Exception("The alpha parameter must be greater or equal to 0.")
		n = len(X)
		p = len(X[0])
		X = np.array(X)
		Xin = np.hstack([ np.ones([X.shape[0], 1]), X ])

		# Estimators of parameters
		self.beta = np.linalg.solve(np.dot(np.transpose(Xin), Xin) + alpha * np.identity(p + 1), np.dot(np.transpose(Xin), Y))
		my = sum(Y) / n

		# Accuracy estimators
		self.SCR = sum((Y - np.dot(Xin, np.transpose(self.beta)))**2)
		self.SST = sum((Y - np.repeat(my, n))**2)
		residue = self.SCR / self.SST
		self.R2 = 1.0 - residue
		self.R2a = 1.0 - (n / (n - p)) * residue

		self.fitted = True

		if verbose:
			print("Accuracy of " + self.name + " with alpha=" + str(alpha) + " :")
			print("-" * 30)
			print("Multiple R-squared \t" + str(self.R2))
			print("Adjusted R-squared \t" + str(self.R2a))
			print("-" * 30)

	def predict(self, X):
		super(RidgeRegressionModel, self).isfit()
		return [ self.beta[0] + np.dot(X[i], self.beta[1:]) for i in range(len(X)) ]

	def parameters(self):
		super(RidgeRegressionModel, self).isfit()
		return self.beta

	def accuracy(self):
		return [ self.R2, self.R2a ]

# A ridge linear regression over n-D value
class KernelRidgeRegressionModel(Model):

	name = "Kernel Ridge Regression"

	def __init__(self):
		Model.__init__(self)
		self.beta = []
		self.kernelFun = None
		self.kernelMat = [[]]
		self.Xtrain = []
		self.Ytrain = []
		self.alpha = 0

	def fit(self, X, Y, alpha=1, kernel='rbf', verbose=False):
		if alpha < 0:
			raise Exception("The alpha parameter must be greater or equal to 0.")
		self.kernelFun = GetKernelParameter(kernel)

		n = len(X)
		p = len(X[0])
		self.Xtrain = np.array(X)
		self.alpha = alpha
		self.Ytrain = np.array(Y)
		self.kernelMat = np.array([[self.kernelFun(xi,xj) for xj in self.Xtrain] for xi in self.Xtrain])

		# Estimators of parameters
		self.beta = np.dot(self.Xtrain.T, np.linalg.pinv(self.kernelMat + alpha * np.identity(n)).dot(Y))
		self.fitted = True

		if verbose:
			print("Parameters of " + self.name + " with alpha=" + str(alpha) + " :")
			print("-" * 30)
			if type(kernel) is str:
				print("Kernel \t" + kernel)
			else:
				print("Kernel \tcustom")
			print("-" * 30)

	def predict(self, X):
		super(KernelRidgeRegressionModel, self).isfit()
		Kern = np.array([[self.kernelFun(xi,xj) for xj in self.Xtrain] for xi in X])
		inv = np.linalg.pinv(self.kernelMat + self.alpha * np.identity(len(self.kernelMat)))
		right = np.dot(inv, self.Ytrain)
		return np.dot(Kern, right)

	def parameters(self):
		super(KernelRidgeRegressionModel, self).isfit()
		return self.beta


# A simple Bayesian linear regression over 1-D value
class SimpleBayesianLinearRegressionModel(Model):

	name = "Bayesian Linear Regression"

	def __init__(self):
		Model.__init__(self)
		self.beta0 = 0
		self.beta1 = 0
		self.tau = 2

	def fit(self, X, Y, mu_0=0, mu_1=0, tau_0=1, tau_1=1, alpha=2, gamma=1, n_iter=100, verbose=False):
		# The conditional distribution over beta0 is a normal distribution
		def sampling_beta0(beta1, x, y, mu0, tau, tau0):
			N = len(y)
			assert len(x) == N
			var = 1.0 / (tau0 + tau * N)
			mean = (tau0 * mu0 + tau * sum(y - beta1 * x)) * var
			return np.random.normal(mean, math.sqrt(var))

		# The conditional distribution over beta1 is a normal distribution
		def sampling_beta1(beta0, x, y, mu1, tau, tau1):
			N = len(y)
			assert len(x) == N
			var = 1.0 / (tau1 + tau * sum(x * x))
			mean = (tau1 * mu1 + tau * sum((y - beta0) * x)) * var
			return np.random.normal(mean, math.sqrt(var))

		# The conditional distribution over tau is a Gamma distribution
		def sampling_tau(y, x, beta0, beta1, alpha, gamma):
			N = len(y)
			param1 = alpha + N / 2.0
			residue = y - beta0 - beta1 * x
			param2 = gamma + sum(residue * residue) / 2.0
			return np.random.gamma(param1, 1.0 / param2)

		X = np.asarray(X)
		Y = np.asarray(Y)

		# Three-stages Gibbs sampling
		for it in range(n_iter):
			self.beta0 = sampling_beta0(self.beta1, X, Y, mu_0, self.tau, tau_0)
			self.beta1 = sampling_beta1(self.beta0, X, Y, mu_1, self.tau, tau_1)
			self.tau = sampling_tau(Y, X, self.beta0, self.beta1, alpha, gamma)

		self.fitted = True

		if verbose:
			print("Parameters of " + self.name + " :")
			print("-" * 30)
			print("Beta 0 \t\t" + str(self.beta0))
			print("Beta 1 \t\t" + str(self.beta1))
			print("Precision \t" + str(self.tau))
			print("-" * 30)

	def predict(self, X, noise=False):
		super(SimpleBayesianLinearRegressionModel, self).isfit()
		if not(noise):
			return [ self.beta0 + self.beta1 * X[i] for i in range(len(X)) ]
		return [ np.random.normal(self.beta0 + self.beta1 * X[i], 1 / math.sqrt(self.tau)) for i in range(len(X)) ]

	def parameters(self):
		super(SimpleBayesianLinearRegressionModel, self).isfit()
		return [ self.beta0, self.beta1, self.precision ]

# A polynomial regression over 1-D value
class PolynomialRegressionModel(Model):

	name = "Polynomial Regression"

	def __init__(self):
		self.fitted = False
		self.a = []

	def fit(self, X, Y, deg, verbose=False):
		X = np.array(X)
		self.a = np.polyfit(X, Y, deg)

		self.fitted = True

		if verbose:
			print("Parameters of " + self.name + " with " + str(deg) + " degrees :")
			print("-" * 30)
			for i in range(len(self.a)):
				print("a" + str(i) + "\t" + str(self.a[i]))
			print("-" * 30)

	def predict(self, X):
		return [ np.polyval(self.a, X[k]) for k in range(len(X)) ]

# A SVM regression over n-D value
class SupportVectorRegressionModel(Model):

	name = "Support Vector Regression"

	def __init__(self):
		self.fitted = False
		self.model = None

	# Need to handle custom kernels
	def fit(self, X, Y, C=1, gamma=0.1, kernel='rbf', verbose=False):
		X = np.array(X)
		kernelFun = GetKernelParameter(kernel)
		SVM = SVR(kernel=kernel, C=C, gamma=gamma)
		self.model = SVM.fit(X, Y)

		self.fitted = True

		if verbose:
			print("Parameters of " + self.name + " with C=" + str(C) + " and gamma=" + str(gamma) + " :")
			print("-" * 30)
			print("-" * 30)

	def predict(self, X):
		return self.model.predict(X)

# A Gaussian process regression over n-D value
class GaussianProcessRegressionModel(Model):

	name = "Gaussian Process Regression"

	def __init__(self):
		self.fitted = False
		self.model = None

	def fit(self, X, Y, alpha=0.0, verbose=False):
		X = np.array(X)
		kernel = 1.0 * GPKernels.RBF(length_scale=100.0, length_scale_bounds=(1e-2, 1e3)) + GPKernels.WhiteKernel(noise_level=1, noise_level_bounds=(1e-10, 1e+1))
		gp = GaussianProcessRegressor(kernel=kernel, alpha=alpha)
		self.model = gp.fit(X, Y)
		self.fitted = True

		if verbose:
			print("Parameters of " + self.name + " :")
			print("-" * 30)
			print("-" * 30)

	def predict(self, X):
		return self.model.predict(X)
