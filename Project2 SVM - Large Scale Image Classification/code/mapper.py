#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

# Use the Adagrad (with pegasos) algorithm to train the W in svm 
# change the New_dimension variable

import sys
import numpy as np
import math
from scipy.optimize import minimize


DIMENSION = 400  # Dimension of the original data.
CLASSES = (-1, +1)   # The classes that we are trying to predict.
New_dimension = 6000 # dimension after transform


## Non-transform
# def transform(x_original):
# 	x_transformed = x_original
# 	return x_transformed

## Gaussian kernel

np.random.seed(seed = 2015) # THIS line is VERY important!

# for gaussian kernel
# mean = np.zeros(DIMENSION)
# sigma = 2
# cov = np.eye(DIMENSION) / np.square(sigma) # sample omega for gaussian
# omega = np.random.multivariate_normal(mean, cov, New_dimension) # sample omega for gaussian


# for laplacian kernel
gamma = 0.7

omega = gamma * np.random.standard_cauchy((New_dimension, DIMENSION))

# u_uniform = np.random.uniform(0.0, 1.0, (New_dimension, DIMENSION))
# omega = gamma * np.tan( math.pi * ( u_uniform - 0.5 ) )

# for cauchy kernel
# omega = np.random.laplace(loc=0.0, scale = sigma, size = (New_dimension, DIMENSION) )


b = np.random.uniform(0, 2*math.pi, New_dimension)


def transform(x_original):
	# omega is new_dimension * old_dimension matrix
	x_transformed = math.sqrt(2) * np.cos( np.inner(omega, x_original) + b ) / math.sqrt(New_dimension)
	return x_transformed





if __name__ == "__main__":
	# Initialization
	# New_dimension = 400 # dimension after transform
	Lambda = 0.00002 # the regularization parameter \lambda, s.t. the L2 norm of W is less than 1/sqrt(Lambda)
	# optimal lambda (for adagrad & pegasos with constrain): 0.000001 with score: 0.793222
	# optimal lambda (for adagrad & pegasos without constrain): 0.000001 with score: 0.793022
	Eta = 1
	W = np.zeros(New_dimension, dtype=float) # save the parameter W, 
	S = np.ones(New_dimension, dtype=float) # save the diag(G)
	Grad = np.zeros(New_dimension, dtype=float) # save gradient of f(W) at each step
	t=0 #


	# for the constrain in Malanobis space
	# def Mdist(x, xt, Gt):
	# 	w_new = x - xt
	# 	result = w_new * w_new
	# 	result = np.dot(result, Gt)
	# 	return result
	# cons = ({'type':'ineq', 'fun' : lambda x: np.array( [  1/Lambda - np.dot(x,x)  ] )})


	# Update W after meet new data point
	for line in sys.stdin:
	    line = line.strip()
	    (label, x_string) = line.split(" ", 1)
	    label = int(label)
	    x_original = np.fromstring(x_string, sep=' ', dtype=float)
	    x = transform(x_original)  # Use our features.
	    # x is new data point, label is the label for new data point
	    ##########################

	    
	    t = t + 1 # update time step
	    # if this new data point is classified correctly, do not update W, else compute f(W) and update W
	    error_tmp = label * np.dot(x,W)
	    if(error_tmp>=1.0): # do not need to update W
	    	W = W
	    else: # update W
	    	# Grad = - label * x
	    	Grad = Lambda * W - label * x
	    	## update each location of W
	    	
	    	S = S + np.square(Grad)
	    	# Eta = 1.0 / np.sqrt(t)
	    	Eta = 1.0 / (Lambda * t)
	    	W = W - Eta / np.sqrt(S) * Grad
	    	# W = W - Eta * Grad

	    	# res = minimize(Mdist, np.zeros(New_dimension), args=(W, np.sqrt(S)), method='SLSQP', constraints=cons)
	    	# W = res.x
	    	# print W
	    	W = W * min(1, 1.0 / ( np.linalg.norm(W) * np.sqrt(Lambda) ) )


	print "%d\t%s" % (1, str(W.tolist()).strip("[]"))

