#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import sys

N = 20001
# Number of shingles
b = 50
# b bands
r = 20
# r rows per band
n = b * r
# Number of rows in signature matrix
# Number of min-hash functions
Prime = 150000001
# Big Prime http://www.prime-numbers.org/

if __name__ == "__main__":
    # VERY IMPORTANT:
    # Make sure that each machine is using the
    # same seed when generating random numbers for the hash functions.
    np.random.seed(seed = 2015)
    rand_a = np.random.randint(N, size = n)   # rand_a[0...n-1]
    rand_b = np.random.randint(N, size = n)   # rand_b[0...n-1]
    # Min-Hash Function Hi(r) := rand_a[i] * r + rand_b[i] mod N

    rand_c = np.random.randint(N, size = (b, r))   # rand_c[0...b-1][0...r-1]
    rand_d = np.random.randint(N, size = b)   # rand_d[0...b-1]
    # Linear-Hash Function Hi(s) := Sum(rand_c[i][j] * Sj) + rand_d[i] mod N


    for line in sys.stdin:
        line = line.strip()
        video_id = int(line[6:15])
        shingles = np.fromstring(line[16:], dtype = np.int, sep = " ")

        signature = np.full(n, np.iinfo(np.int64).max, dtype = np.int)
        for shingle in shingles:
            for i in range(0, n):
                minhash = (rand_a[i] * shingle + rand_b[i]) % N
                signature[i] = min(signature[i], minhash)

        for i in range(0, b):
            linearhash = 0
            for j in range(0, r):
                linearhash = linearhash + rand_c[i][j] * signature[i * r + j]
            linearhash = linearhash + rand_d[i]
            bucked_id = linearhash % Prime
            print "%d\t%d\t%s" % (bucked_id, video_id, line[16:])
