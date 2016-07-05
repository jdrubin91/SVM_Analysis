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
    
    for file1 in files:
        print file1
        with open(file1) as F:
            N = 0.0
            TFs = F.readline().strip().split()[3:]
            vectors = [[0.0]*len(TFs)] * len(TFs)
            for line in F:
                print N
                N += 1.0
                line = [float(i) for i in line.strip().split()[3:]]
                for i in range(len(line)):
                    if 'eGFP' not in TFs[i]:
                        for j in range(len(line)):
                            if line[i] > 0 and line[j] > 0:
                                vectors[i][j] += 1.0
                                
            
        vectors = [[i/N for i in TF] for TF in vectors]
        vectors = np.array(vectors)
        labels = [i for i in TFs if 'eGFP' not in i]
        
        # Generate random features and distance matrix.
        x = len(labels)
        D = scipy.zeros([x,x])
        for i in range(x):
            for j in range(x):
                for k in range(x):                    
                    D[i,j] += (vectors[i][k] - vectors[j][k])**2
                D[i,j] = math.sqrt(D[i,j])
        print D
        
        
        # Compute and plot first dendrogram.
        fig = pylab.figure(figsize=(8,8))
        ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
        Y = sch.linkage(D, method='centroid')
        Z1 = sch.dendrogram(Y, orientation='right')
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Compute and plot second dendrogram.
        ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
        Y = sch.linkage(D, method='single')
        Z2 = sch.dendrogram(Y)
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        # Plot distance matrix.
        axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
        idx1 = Z1['leaves']
        idx2 = Z2['leaves']
        D = D[idx1,:]
        D = D[:,idx2]
        im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu)
        axmatrix.set_xticks([])
        axmatrix.set_yticks([])
        
        # Plot colorbar.
        axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
        pylab.colorbar(im, cax=axcolor)
        fig.show()
        fig.savefig(savedir + file1.split('/')[-1] + '_dendrogram.png')

if __name__ == "__main__":
    run()