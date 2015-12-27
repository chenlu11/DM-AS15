#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

# Reducer: Weighted K-Means
import sys
import numpy as np
d = 500    # feature dimension
k = 100    # number of clusters

if __name__ == "__main__":
    D = np.loadtxt(sys.stdin, delimiter=' ', usecols=np.arange(1, 502, dtype = np.int))
    n = int(D.shape[0])    # total sample size
    rand = np.random.choice(n, k, replace = False)
    centroid = D[rand, 1:]
    epsilon = float("inf")
    
    while epsilon > 0.01:
        update = np.empty([k, d])
        count = np.zeros(k)
        for i in range(n):
            delta = centroid - D[i, 1:]
            dist_2 = np.einsum('ij,ij->i', delta, delta)
            c = np.argmin(dist_2)
            update[c] = update[c] + D[i, 0] * D[i, 1:]
            count[c] = count[c] + D[i, 0]
        for i in range(k):
            if count[i] == 0:
                update[i] = centroid[i]
            else:
                update[i] = update[i] / count[i]
        diff = centroid - update
        epsilon = np.linalg.norm(diff, np.inf)
        centroid = update

    for i in range(k):
        print "%s" % (str(centroid[i].tolist()).strip('[]').replace(',',''))
