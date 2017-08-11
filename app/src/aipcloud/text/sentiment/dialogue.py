import time

from ...statistics import regression
from ...exceptions import UnloadedException

class DialogueSentimentAnalyzer:

	def __init__(self):
		self.loaded = False
		self.analyzer = SentenceSentimentAnalyzer()

	def load(self):
		self.analyzer.load()
		self.loaded = True

	def analyze(self, listA, listB, verbose=False):
		if not(self.loaded):
			raise UnloadedException()
		if abs(len(listA) - len(listB)) >= 2:
			print("Input lists are not a dialogue.")
			return

		eltime = time.time()

		Na = len(listA)
		Nb = len(listB)
		N = max(Na, Nb)

		mainList = listA
		if Nb > Na:
			mainList = listB

		classesA = []
		classesB = []
		weightsA = []
		weightsB = []
		lerpA = []
		lerpB = []

		for i in range(N):
			if i < Na:
				anA = self.analyzer.analyze(listA[i])
				w = abs(anA[2] - anA[0]) + abs(anA[1] - anA[0]) + abs(anA[2] - anA[1])
				w /= 3
				weightsA.append(w)
				classesA.append(anA)
				print(str(w) + " - " + listA[i])
				print(anA)
				lerpA.append((anA[2] + anA[1]) / 3.0)
			if i < Nb:
				anB = self.analyzer.analyze(listB[i])
				w = abs(anB[2] - anB[0]) + abs(anB[1] - anB[0]) + abs(anB[2] - anB[1])
				w /= 3
				weightsB.append(w)
				classesB.append(anB)
				lerpB.append((anB[2] + anB[1]) / 3.0)

		negA = [ classesA[i][0] * weightsA[i] for i in range(Na) ]
		midA = [ classesA[i][1] * weightsA[i] for i in range(Na) ]
		posA = [ classesA[i][2] * weightsA[i] for i in range(Na) ]
		negB = [ classesB[i][0] * weightsB[i] for i in range(Nb) ]
		midB = [ classesB[i][1] * weightsB[i] for i in range(Nb) ]
		posB = [ classesB[i][2] * weightsB[i] for i in range(Nb) ]
		sumWeightsA = sum(weightsA)
		sumWeightsB = sum(weightsB)

		distribA = [ sum(negA) / sumWeightsA, sum(midA) / sumWeightsA, sum(posA) / sumWeightsA ]
		distribB = [ sum(negB) / sumWeightsB, sum(midB) / sumWeightsB, sum(posB) / sumWeightsB ]
		accuracyA = abs(distribA[0] - distribA[1]) + abs(distribA[2] - distribA[1])
		accuracyA = accuracyA**(1/3)
		accuracyB = abs(distribB[0] - distribB[1]) + abs(distribB[2] - distribB[1])
		accuracyB = accuracyB**(1/3)
		accuracy = (accuracyA + accuracyB) / 2.0

		regModel = regression.SimpleLinearRegressionModel()
		regModel.fit(range(Na), lerpA)
		slopeA = regModel.parameters()[1] * Na
		regModel.fit(range(Nb), lerpB)
		slopeB = regModel.parameters()[1] * Nb

		estimators = [ accuracyA, accuracyB, accuracy, slopeA, slopeB ]

		if verbose:
			eltime = time.time() - eltime
			print("Time to analyze : {:6.5f} second(s).".format(eltime))

		return distribA, distribB, estimators
