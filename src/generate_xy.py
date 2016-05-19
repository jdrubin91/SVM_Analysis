__author__ = 'Jonathan Rubin'

import numpy as np

def run(directory):
    outdir = directory + 'temp.txt'
    with open(outdir) as F:
        feature_names = F.readline().split()
        Y = eval(F.readline())
        X = eval(F.readline())
    d = dict()
    for i in range(len(Y)):
        if Y[i] == 1:
            d[i] = list()
    while len(d) < sum(Y)*2:
        d[int(np.random.uniform(0,len(Y)))] = list()
    indexes = list()
    for key in d:
        indexes.append(key)
    Y1 = list()
    X1 = list()
    for item in indexes:
        Y1.append(Y[item])
        X1.append(X[item])
        
    return X1,Y1,feature_names