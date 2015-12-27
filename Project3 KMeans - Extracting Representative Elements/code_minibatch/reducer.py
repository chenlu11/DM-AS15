#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
from sklearn.cluster import MiniBatchKMeans

if __name__ == "__main__":
	data = np.loadtxt(sys.stdin, delimiter=' ', usecols=np.arange(1, 501, dtype = np.int))
	mbk = MiniBatchKMeans(n_clusters = 100)
	mbk.fit(data)
	cluster_centers = mbk.cluster_centers_

	num_center = cluster_centers.shape[0]
	for i in range(num_center):
		center = cluster_centers[i,:]
		print "%s" % str(center.tolist()).strip('[]').replace(',','')


	