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

bidirectional = '/scratch/Shares/dowell/EMG_out_files/SRR639050-1_divergent_classifications.bed'
TF = '/scratch/Shares/dowell/ENCODE/SVM/IMR90/TF_ChIP-Seq/ENCFF002CVI.sorted.bed.cut'
directory = '/scratch/Shares/dowell/ENCODE/SVM/IMR90/'

def create_tempfiles():
    #histonelist = list()
    histonelist = [bidirectional]
    for folder in os.listdir(directory):
        if 'H' in folder[0]:
            for file1 in os.listdir(directory + folder):
                if 'bed' in file1:
                    histonelist.append(directory + folder + '/' + file1)

    for item in histonelist:
        os.system("bedtools intersect -c -a " + TF + " -b " + item + " > " + directory + "SVM_Analysis_out/" + item.split('/')[-1])


def create_SVM_arrays():
    outdir = directory + 'SVM_Analysis_out/'
    Y = list()
    i = 0
    with open(outdir + bidirectional.split('/')[-1]) as F:
        for line in F:
            i += 1
            if int(line.strip().split()[-1]) > 0:
                Y.append(1)
            else:
                Y.append(0)
    
    X = list()
    for j in range(i):
        X.append([])
    feature_names = list()
    for files in os.listdir(outdir):
        if not bidirectional.split('/')[-1] in files:
            print files
            feature_names.append(files)
            with open(outdir + files) as F:
                temp = list()
                for line in F:
                    temp.append(float(line.strip().split()[-1]))
                temp = [k/max(temp) for k in temp]
                for l in range(i):
                    X[l].append(temp[l])
                
    outfile = open(directory + 'temp.txt','w')
    for name in feature_names:
        outfile.write(name + '\t')
    outfile.write('\n')
    outfile.write('[')
    for val in Y:
        outfile.write(str(val) + ',')
    outfile.write(']')
    outfile.write('\n[')
    for val in X:
        outfile.write(str(val) + ',')
    outfile.write(']')
    
def generate_XY():
    outdir = directory + 'temp.txt'
    with open(outdir) as F:
        feature_names = F.readline().split()
        Y = eval(F.readline())
        X = eval(F.readline())
    return X,Y,feature_names
    
def test(X,Y):    
    i = int(len(X)*.8)
    
    d = dict()
    while len(d) < i:
        d[int(np.random.uniform(0,len(X)))] = list()

    indexes = list()
    for key in d:
        indexes.append(key)
    
    Y2 = list()
    X2 = list()
    for item in indexes:
        Y2.append(Y[item])
        X2.append(X[item])
        
    clf = svm.SVC()
    clf.fit(X2, Y2)
    
    Y3 = list()
    X3 = list()
    for l in range(len(X)):
        if not l in d:
            Y3.append(Y[l])
            X3.append(X[l])
    
    c = 0.0
    P = 0.0
    for j in range(len(X3)):
        if clf.predict(X3[j])[0] == 1:
            P += 1.0
            if Y3[j] == 1:
                c += 1.0
                
    p = c/P
    r = c/sum(Y3)
    print 'c,P,r,len(Y3),sum(Y3)',c,P,r,len(Y3),sum(Y3)   
    print 'F1 score: ', 2*((p*r)/(p+r))
    
    
def recursive_feature_elimination(X,Y):
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
    
def univariate_feature_selection(X,Y,feature_names):
    ufs = SelectKBest(chi2,k="all").fit(X,Y)
    
    #print dir(ufs)
    outfile = open(directory + 'univariate_feature_selection.txt','w')
    for i in range(len(feature_names)):
        outfile.write(feature_names[i] + '\t' + str(ufs.scores_[i]) + '\t' + str(ufs.pvalues_[i]) + '\n')
    #for feature in feature_names:
    #    outfile.write(feature + '\t')
    #outfile.write('\n')
    #for score in ufs.scores_:
    #    outfile.write(str(score) + '\t')
    #outfile.write('\n')
    #for pval in ufs.pvalues_:
    #    outfile.write(str(pval) + '\t')

def iterative_test(X,Y):
    ufs = SelectKBest(chi2,k=1).fit(X,Y)

if __name__ == "__main__":
    #create_tempfiles()
    #create_SVM_arrays()
    X,Y,feature_names = generate_XY()
    test(X,Y)
    #univariate_feature_selection(X,Y,feature_names)