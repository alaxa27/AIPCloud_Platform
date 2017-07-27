# AIPCloud
#
# Author : Maxime Jumelle
# Date : 05/07/2017

def TwoStageGibbsSampling(cond1, cond2, n_iter=100, thin=1):
	x = 0
	y = 0
	for i in xrange(n_iter):
		for j in xrange(thin):
			x = cond1(y)
			y = cond2(x)
	return y
