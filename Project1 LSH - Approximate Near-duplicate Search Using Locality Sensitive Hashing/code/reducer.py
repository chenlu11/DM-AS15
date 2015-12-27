#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import sys

def check_similarity(shingles1, shingles2, threshold):
    interset = np.intersect1d(shingles1, shingles2)
    union = np.union1d(shingles1, shingles2)
    jaccard_similarity = np.size(interset) * 1.0 / np.size(union)
    if (jaccard_similarity >= threshold):
        return True
    else:
        return False

def print_duplicates(videos, map):
    unique = np.unique(videos)
    for i in xrange(len(unique)):
        for j in xrange(i + 1, len(unique)):
            if (check_similarity(map[unique[i]], map[unique[j]], 0.9)):
                print "%d\t%d" % (min(unique[i], unique[j]),
                                  max(unique[i], unique[j]))

last_key = None
key_count = 0
duplicates = []
id_shingle_map = {}

for line in sys.stdin:
    line = line.strip()
    key, video_id, shingles = line.split("\t", 2)
    shingles = np.fromstring(shingles, dtype = np.int, sep = " ")

    if last_key is None:
        last_key = key

    if key == last_key:
        duplicates.append(int(video_id))
        id_shingle_map[int(video_id)] = shingles
    else:
        # Key changed (previous line was k=x, this line is k=y)
        print_duplicates(duplicates, id_shingle_map)
        duplicates = [int(video_id)]
        id_shingle_map = {}
        id_shingle_map[int(video_id)] = shingles
        last_key = key

if len(duplicates) > 0:
    print_duplicates(duplicates, id_shingle_map)
