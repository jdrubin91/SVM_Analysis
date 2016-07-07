__author__ = 'Jonathan Rubin'

import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt
from operator import itemgetter
import numpy as np
from scipy.cluster.hierarchy import dendrogram,linkage
import math
import scipy
import pylab
import scipy.cluster.hierarchy as sch

def run():
    file1 = '/scratch/Users/joru1876/files/ENCFF001UWQ.bed_ChIP.bed'
    file2 = '/scratch/Users/joru1876/files/SRR1552480-1_divergent_classifications.bed_ChIP.bed'
    savedir = '/scratch/Users/joru1876/files/'
    
    files = [file1,file2]
    
    vectors = list()
    
    for file1 in files:
        print file1
        with open(file1) as F:
            N = 0.0
            TFs = F.readline().strip().split()[3:]
            indexes = [i for i in range(len(TFs)) if 'eGFP' in TFs[i]]
            TFs = [i for i in TFs if 'eGFP' not in i]
            vector = [[0.0]*len(TFs)] * len(TFs)
            for line in F:
                N += 1.0
                line = [float(i) for i in line.strip().split()[3:]]
                i = 0
                for index in indexes:
                    line.pop(index-i)
                    i += 1
                for i in range(len(line)):
                    for j in range(len(line)):
                        if line[i] > 0 and line[j] > 0:
                            vector[i][j] += 1.0
                                
        print "done parsing"
        vector = [[i/N for i in TF] for TF in vector]
        labels = [i for i in TFs if 'eGFP' not in i]
        vectors.append(vector)
        print "done with: ", file1

        x = len(labels)
        print len(labels)
        print len(vectors)
        L = list()
        for i in range(x):
            L.append([])
            for j in range(x):
                if vectors[1][i][j] == 0 or vectors[0][i][j] == 0:
                    L[i].append(0.0)    
                else:
                    L[i].append(vectors[1][i][j]/vectors[0][i][j])
        
        vectors = np.array(L)
        print vectors
        
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(vectors, cmap=plt.cm.bwr, vmin=-2, vmax=2)
        
        
    # put the major ticks at the middle of each cell
        ax.set_xticks(np.arange(vectors.shape[0])+0.5, minor=False)
        ax.set_yticks(np.arange(vectors.shape[1])+0.5, minor=False)
        
        # want a more natural, table-like display
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        
        ax.set_xticklabels(labels, minor=False, fontsize=8)
        ax.set_yticklabels(labels, minor=False, fontsize=8)
        plt.xticks(rotation=90)
        fig.set_size_inches(20, 15,forward=True)
        plt.savefig(savedir + file1.split('/')[-1] + '.bidirectional_matrix.png')

if __name__ == "__main__":
    run()