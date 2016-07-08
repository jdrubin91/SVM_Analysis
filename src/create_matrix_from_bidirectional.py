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
from numpy.ma import masked_array
import matplotlib.colors as mcolors

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

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
            vector = np.zeros(shape=(len(TFs)-1,len(TFs)-1))
            for line in F:
                N += 1.0
                line = [float(i) for i in line.strip().split()[3:]]
                i = 0
                #if line[-1] == 0:
                for index in indexes:
                    line.pop(index-i)
                    i += 1
                for i in range(len(line)-1):
                    for j in range(len(line)-1):
                        if line[i] > 0 and line[j] > 0:
                            vector[i][j] += 1.0
                                
        print "done parsing"
        vector = [[i/N for i in TF] for TF in vector]
        labels = [i.split('.')[0] for i in TFs if 'TSS' not in i]
        vectors.append(vector)
        print "done with: ", file1

    x = len(labels)
    L = list()
    for i in range(x):
        L.append([])
        for j in range(x):
            if vectors[1][i][j] == 0 or vectors[0][i][j] == 0:
                L[i].append(0.0)    
            else:
                L[i].append(vectors[1][i][j]/vectors[0][i][j])

    vectors = np.array(L)
    outfile = open(savedir+'dendrogram.txt','w')
    for item in labels:
        outfile.write(item + '\t')
    for i in range(len(vectors)):
        outfile.write('\n')
        for j in range(len(vectors)):
            outfile.write(str(vectors[i][j]) + '\t')
    outfile.close()
            
#    d = np.zeros((vectors.shape[1],vectors.shape[1]))
#    for i in range(vectors.shape[1]):
#        for j in range(vectors.shape[1]):
#            d[i,j] = np.sum(np.abs(vectors[:,i]-vectors[:,j]))
#    y=linkage(d,method="average")
#    z=dendrogram(y,no_plot=True)
#    idx=z["leaves"]
#    vectors=vectors[:,idx]    
#    
#    
#    fig, ax = plt.subplots()
#    heatmap = ax.pcolor(vectors, cmap=plt.cm.bwr, vmin=-2, vmax=2)
#    
#    
## put the major ticks at the middle of each cell
#    ax.set_xticks(np.arange(vectors.shape[0])+0.5, minor=False)
#    ax.set_yticks(np.arange(vectors.shape[1])+0.5, minor=False)
#    
#    # want a more natural, table-like display
#    ax.invert_yaxis()
#    ax.xaxis.tick_top()
#    
#    ax.set_xticklabels(labels, minor=False, fontsize=8)
#    ax.set_yticklabels(labels, minor=False, fontsize=8)
#    plt.xticks(rotation=90)
#    fig.set_size_inches(20, 15,forward=True)
#    plt.savefig(savedir + 'bidirectional_matrix.png')

    # Compute and plot first dendrogram.
    D = vectors
    fig = pylab.figure(figsize=(12,12))
    #ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
    #Y = sch.linkage(D, method='ward')
    #Z1 = sch.dendrogram(Y, orientation='right')
    #ax1.set_xticks([])
    #ax1.set_yticks([])
    
    # Compute and plot second dendrogram.
    ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
    Y = sch.linkage(D, method='ward')
    Z2 = sch.dendrogram(Y)
    ax2.set_xticks([])
    ax2.set_yticks([])
    c = mcolors.ColorConverter().to_rgb
    rvb = make_colormap([c('blue'), c('white'), 0.6, c('white'), c('red'), 1, c('red')])
    # Plot distance matrix.
    axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
    idx1 = Z2['leaves']
    idx2 = Z2['leaves']
    D = D[idx1,:]
    D = D[:,idx2]
    im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=rvb,vmax=6,vmin=0)
    axmatrix.set_xticks([])
    #axmatrix.set_yticks([])
    axmatrix.set_yticks(range(0,vectors.shape[0]))
    axmatrix.yaxis.tick_left()
    axmatrix.set_yticklabels([labels[val] for val in idx1],minor=False,fontsize=10)
    
    # Plot colorbar.
    axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
    pylab.colorbar(im, cax=axcolor)
    fig.show()
    fig.savefig(savedir + 'bidirectional_dendrogram.png')

if __name__ == "__main__":
    run()