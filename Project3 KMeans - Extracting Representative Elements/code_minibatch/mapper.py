#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

# use the minibatch-kmeans in mapper

import sys
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from math import ceil


if __name__ == "__main__":

	data = np.loadtxt(sys.stdin, delimiter=' ', usecols=np.arange(0, 500, dtype = np.int))
	mbk = MiniBatchKMeans(n_clusters=200, batch_size=100000)
	mbk.fit(data)
	cluster_centers = mbk.cluster_centers_

	num_center = cluster_centers.shape[0]
	for i in range(num_center):
		center = cluster_centers[i,:]
		print "%d %s" % (1, str(center.tolist()).strip('[]').replace(',',''))
		













