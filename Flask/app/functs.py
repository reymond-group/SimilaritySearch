import numpy as np
import os
import subprocess as sub
from operator import itemgetter
from rdkit.Chem import AllChem as Chem
from rdkit.Chem import rdMolDescriptors
import pickle
from annoy import AnnoyIndex


def fp_calc(smile):
    """returns MXfpfp of the given smiles
    
    Arguments:        
        smile {string} -- smile of the query ligand
    
    Returns:
        string -- query ligand MXfp
    """

    with open('temp_query_smiles.smi', '+w') as outFIle:
        outFIle.write(smile + ' query_ligand')
    
    proc=sub.Popen(['java', '-cp', 'app/static/MXFP/2Dtopoguassfp.jar', 'bin.write_topoguassfp2', 
        '-i', 'temp_query_smiles.smi', '-o', 'temp_query_ligand.fp', 
        '-scaleFactors 0.5_1_0.5_1_1_1_1'], stdout=sub.PIPE)
    proc.wait()

    with open('temp_query_ligand.fp') as inFile:
        for line in inFile:
            line = line.strip()
            line = line.split(' ')
            fp = line[2]
    os.remove('temp_query_smiles.smi')
    os.remove('temp_query_ligand.fp')

    return fp

def similarity_search_annoy(db, smile, number_of_hits):
    """returns n hits of the given query ligand  
    
    Arguments:
        db {string} -- NLP or NLC
        smile {string} -- smile of the query ligand
        number_of_hits {integer} -- number of required hits
    
    Returns:
        list -- n NN of the query molecule according to MXfp 
    """

    data_path = '/SimilaritySearchData/'
        
    fp = fp_calc(smile)
    query_fp = np.array(list(map(int, fp.split(';')))).reshape(1, -1)
    
    # MXFP is a vectors of 217 elements
    f = 217
    u = AnnoyIndex(f, metric='manhattan') 

    u.load(data_path + 'Non-Lipinski-{}.MXfp_annoy'.format(db))
    NNs = u.get_nns_by_vector(query_fp[0], int(number_of_hits), search_k=-1, include_distances=True)
    results = []

    findID = pickle.load(open(data_path + 'Non-Lipinski-{}.MXfp_dictionary'.format(db), 'rb'))
    
    for i, NN in enumerate(NNs[0]):
        results.append((findID[NN], round(NNs[1][i],2)))

    return (results)