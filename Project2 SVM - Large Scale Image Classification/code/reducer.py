#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

# change the New_dimension variable

import logging
import sys
import numpy as np

if __name__ == "__main__":
	New_dimension = 6000
	W_global = np.zeros(New_dimension, dtype=float)
	count = 0.0
	for line in sys.stdin:
	    line = line.strip()
	    null, w = line.split("\t", 1)
	    w = np.fromstring(w,sep=", ")
	    W_global = W_global + w
	    count = count + 1

	W_global = W_global / count  

	print "%s" % str(W_global.tolist()).strip('[]').replace(',','')