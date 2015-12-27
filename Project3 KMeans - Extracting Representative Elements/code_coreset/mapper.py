#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

# Mapper: Coreset construction via Adaptive Sampling
import sys
import numpy as np
epsilon = 0.1 # lower bound: 1 - epsilon & upper bound: 1 + epsilon
delta = 0.1 # with probability at least 1 - delta lower & upper bound hold true
d = 500    # feature dimension
k = 100    # number of clusters

# return the index of closest point of x in B and [d(x, B)]^2
def distance(x, B):
    deltas = B - x
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.array([np.argmin(dist_2), np.min(dist_2)])

if __name__ == "__main__":

    D = np.loadtxt(sys.stdin, delimiter=' ', usecols=np.arange(0, 500, dtype = np.int))
    n = int(D.shape[0])    # total sample size
    D_prime = np.arange(n)
    B = np.empty([0],dtype=int)
    dist_B = np.zeros(n)    # store the dist(x,B)
    m = np.zeros(n)    # store m(x)
    b = np.zeros(n)    # if x in Db, then b[x] = b

    #beta = int(10 * d * k * np.log(1/delta))
    beta = 1

    # construct the sampling rule
    while (D_prime.shape[0] > beta):
        S = np.random.choice(D_prime, beta, replace = False)    # sample S uniformly from D'
        
        B = np.append(B, S)    # take the union of B and S, need to remove duplicate later
        
        dist_S = np.zeros(D_prime.shape[0])    # used to store d(x, S)^2 to decide which pts to remove
        for i in range(D_prime.shape[0]):
            dist_S[i] = distance(D[D_prime[i]], D[S])[1]
        remove_index = np.asarray(np.where(dist_S < np.median(dist_S)))   # index of points to remove
        D_prime = np.delete(D_prime, remove_index)    # remove the [|D'|/2] pts closest to S
    B = np.append(B, D_prime)  
    B = np.unique(B)
    size_Db = np.zeros(B.shape[0])
    
    for i in range(D.shape[0]):
        b[i], dist_B[i] = distance(D[i], D[B])
        size_Db[b[i]] = size_Db[b[i]] + 1   # compute |Db|
    
    sum_dist_B = np.sum(dist_B)
    
    # compute m(x)
    for i in range(D.shape[0]):
        m[i] = 5.0/size_Db[b[i]] + dist_B[i]/sum_dist_B
    
    # construct C
    #size_C = 10*int(d*k*np.log(B.shape[0]*B.shape[0])*np.log(1/delta)/epsilon/epsilon)
    size_C = 200
    sum_m = np.sum(m)
    C = np.random.choice(n, size_C, p = m/sum_m, replace = False)
    
    for i in range(size_C):
        tmp = np.insert(D[C[i]], 0, sum_m/size_C/m[C[i]])
        print "%d %s" % (1, str(tmp.tolist()).strip('[]').replace(',',''))
