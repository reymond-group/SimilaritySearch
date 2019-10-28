from annoy import AnnoyIndex
import random
import numpy as np
import _pickle
import sys

# imput: - MXFP results (SMILES ID MXFP properties) 
#        - python dictionary of PubChem {CIDs : SMILES as in PubChem} (optional)
# output: - inputfile_annoy
#         - inputfile_dictionary 

findCID = {}

# MXFP has 217 dimentions
f = 217  

t = AnnoyIndex(f, metric='manhattan') 

if len(sys.argv) == 3:
    Original_id = _pickle.load(open(sys.argv[2], 'rb'))

with open(sys.argv[1]) as inFile:
    for i, line in enumerate(inFile):
        line = line.strip()
        line = line.split(' ')
        fp = np.array(list(map(float, line[2].split(';'))))
        t.add_item(i, fp)
        if len(sys.argv) == 3:
            findCID[i] = (line[1], Original_id[line[1]])
        else:
            findCID[i] = (line[1], line[0])

_pickle.dump(findCID, open('{}_dictionary'.format(sys.argv[1]), 'wb'))

# 50 annoy trees are created
t.build(50) 
t.save('{}_annoy'.format(sys.argv[1]))


