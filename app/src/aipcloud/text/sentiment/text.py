import numpy as np
import time
import matplotlib.pyplot as plt

from .sentence import SentenceSentimentAnalyzer
from ...statistics import regression
from ...exceptions import UnloadedException

class TextSentimentAnalyzer:

	TOP_WORDS = 40000

	def __init__(self):
		self.loaded = False
		self.analyzer = SentenceSentimentAnalyzer()

	def load(self):
		self.analyzer.load()
		self.loaded = True

	def analyze(self, text, verbose=False):
		if not(self.loaded):
			raise UnloadedException()

		eltime = time.time()

		text = text.lower()
		lines = re.split(r"[.;!?]+", text)

		classes = []
		weights = []
		lerp = []

		for line in lines:
			if len(line) > 3:
				an = self.analyzer.analyze(line)
				w = abs(an[2] - an[0]) + abs(an[1] - an[0]) + abs(an[2] - an[1])
				w /= 3
				classes.append(an)
				weights.append(w)
				lerp.append((an[2] + an[1]) / 2.0)

		N = len(classes)
		if N <= 1:
			print("At least two lines are needed.")
			return

		neg = [ classes[i][0] * weights[i] for i in range(N) ]
		mid = [ classes[i][1] * weights[i] for i in range(N) ]
		pos = [ classes[i][2] * weights[i] for i in range(N) ]

		sumWeight = sum(weights)
		distrib = [ sum(neg) / sumWeight, sum(mid) / sumWeight, sum(pos) / sumWeight ]
		accuracy = abs(distrib[0] - distrib[1]) + abs(distrib[2] - distrib[1])
		accuracy = accuracy**(1/3)
		mainLerp = distrib[2] - distrib[0]
		variance = sum([abs(lerp[i+1] - lerp[i]) for i in range(N - 1)]) / (N - 1)

		regModel = regression.SimpleLinearRegressionModel()
		regModel.fit(range(N), lerp)
		slope = regModel.parameters()[1] * N

		if verbose:
			eltime = time.time() - eltime
			print("Time to analyze : {:6.5f} second(s).".format(eltime))

			plt.plot(range(N), neg, color="r")
			plt.plot(range(N), mid, color="b")
			plt.plot(range(N), pos, color="g")
			plt.plot(range(N), np.repeat(distrib[0], N), color="r")
			plt.plot(range(N), np.repeat(distrib[1], N), color="b")
			plt.plot(range(N), np.repeat(distrib[2], N), color="g")
			plt.plot(range(N), lerp, color="black")
			plt.plot([0, N-1], regModel.predict([0, N-1]), color="m")
			plt.show()

		results = [ accuracy, slope, mainLerp, variance ]
		results = np.hstack((distrib, results))
		return results

	def summary(self, inputVector):
		distrib = inputVector[0:3]
		accuracy = inputVector[3]
		slope = inputVector[4]

		frenchClasses = [ "négatif", "neutre", "positif" ]

		summary = "Le texte est "
		if accuracy >= 0.75:
			summary += frenchClasses[np.argmax(distrib)] + "."
		elif accuracy >= 0.5:
			summary += "plutôt neutre "
			argmin = np.argmin(distrib)
			if argmin == 1:
				summary += "avec des grandes variations positives et négatives."
			else:
				summary += frenchClasses[2 - argmin] + "."
		elif accuracy >= 0.35:
			summary += "semble être plutôt neutre "
			argmin = np.argmin(distrib)
			if argmin == 1:
				summary += "avec des grandes variations positives et négatives, "
			else:
				summary += frenchClasses[2 - argmin] + ", "
			summary += "mais l'analyse est moyennement pertinente."
		else:
			summary = "L'analyse n'est pas assez pertinente sur ce texte."

		if accuracy >= 0.35:
			if abs(slope) >= 0.4:
				if slope > 0:
					summary += " Le texte est négatif au début et positif vers la fin."
				else:
					summary += " Le texte est positif au début et négatif vers la fin."
			elif abs(slope) >= 0.12:
				argmin = np.argmin(distrib)
				if slope > 0:
					if argmin == 2:
						summary += " Le texte est neutre au début et positif vers la fin."
					elif argmin == 1:
						summary += " Le texte est négatif au début et neutre vers la fin."
				elif slope < 0:
					if argmin == 0:
						summary += " Le texte est neutre au début et négatif vers la fin."
					elif argmin == 1:
						summary += " Le texte est positif au début et neutre vers la fin."
			else:
				summary += " Le sentiment est constant tout au long du texte."
		return summary
