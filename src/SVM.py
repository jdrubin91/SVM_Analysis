__author__ = 'Jonathan Rubin'

import os
from sklearn import svm
import numpy as np
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from operator import itemgetter

def recursive_feature_elimination(X,Y,directory):
    # Create the RFE object and compute a cross-validated score.
    svc = SVC(kernel="linear")
    # The "accuracy" scoring is proportional to the number of correct
    # classifications
    rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(Y, 2),
                scoring='accuracy')
    rfecv.fit(X, Y)
    
    print("Optimal number of features : %d" % rfecv.n_features_)
    
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.savefig(directory + 'figure.png')
    
def univariate_feature_selection(X,Y,feature_names,directory,TF):
    ufs = SelectKBest(chi2,k="all").fit(X,Y)
    
    #print dir(ufs)
    outfile = open(directory + TF + '_ufs.txt','w')
    outlist = list()
    for i in range(len(feature_names)):
        outlist.append((feature_names[i],ufs.scores_[i],ufs.pvalues_[i]))
    outlist = sorted(outlist,key=itemgetter(1))
    for i in range(len(outlist)):
        outfile.write(outlist[i][0] + '\t' + str(outlist[i][1]) + '\t' + str(outlist[i][2]) + '\n')