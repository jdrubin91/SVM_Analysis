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

def run(files,figures):
    S = dict()
    for file1 in os.listdir(files):
        print file1
        N = 0
        p = 0
        with open(files+file1) as F:
            TFs = F.readline().strip().split()[1:]
            weights = [0.0] * len(TFs)
            b = [0.0] * len(TFs)
            for line in F:
                N += 1.0
                line = [int(i) for i in line.strip().split()[3:]]
                for i in range(len(line)):
                    if line[i] > 0:
                        line[i] = 1.0
                    else:
                        line[i] = 0.0
                if line[0] > 0:
                    p += 1.0
                    b = [b[i] + line[i+1] for i in range(len(line[1:]))]
                weights = [weights[i] + line[i+1] for i in range(len(line[1:]))]
        S[file1.split('.')[0]] = [N,p,TFs,weights,b]
    I = dict()
    print "Done with parsing, starting to analyze"
    for TFi in S:
        if not TFi == 'ZNF274':
            N = S[TFi][0]
            p = S[TFi][1]
            TFs = S[TFi][2]
            weights = S[TFi][3]
            b = S[TFi][4]
            for j in range(len(TFs)):
                TFj = TFs[j]
                if not TFj == 'ZNF274':
                    wj = weights[j]
                    bj = b[j]
                    Ex = (p/N)*(wj/N)*N
                    if Ex == 0:
                        I[TFi + '~' + TFj] = 0.0
                    else:
                        I[TFi + '~' + TFj] = bj/Ex
    
    d1 = dict()
    for pair in I:
        TFi,TFj = pair.split('~')
        if not TFi in d1:
            d1[TFi] = [(TFi,0.0)]
        Si = I[pair]
        Sj = I[TFj + '~' + TFi]
        d1[TFi].append((TFj,math.log(((Si+Sj)/2.0)+0.0001)))
    
    order = list()
    for key in d1:
        i = 0
        for tuple1 in d1[key]:
            i += tuple1[1]
        order.append((key,i))
    
    order = sorted(order,key=itemgetter(1),reverse=True)
    labels = [i for (i,j) in order]
    vectors = list()
    M = list()
    for i in range(len(labels)):
        vectors.append(list())
        for j in range(len(labels)):
            index = [y[0] for y in d1[labels[i]]].index(labels[j])
            vectors[i].append(d1[labels[i]][index][1])
            M.append(d1[labels[i]][index][1])
                
    #vectors = [d1[name][i][1] for name,i in labels,range(len(labels))]
    
    vectors = np.array(vectors)
            
   # fig, ax = plt.subplots()
   # print np.mean(M)+(np.std(M)*2)
   # heatmap = ax.pcolor(vectors, cmap=plt.cm.bwr, vmin=-2, vmax=2)
   # 
   # 
   ## put the major ticks at the middle of each cell
   # ax.set_xticks(np.arange(vectors.shape[0])+0.5, minor=False)
   # ax.set_yticks(np.arange(vectors.shape[1])+0.5, minor=False)
   # 
   # # want a more natural, table-like display
   # ax.invert_yaxis()
   # ax.xaxis.tick_top()
   # 
   # ax.set_xticklabels(labels, minor=False, fontsize=8)
   # ax.set_yticklabels(labels, minor=False, fontsize=8)
   # plt.xticks(rotation=90)
   # fig.set_size_inches(20, 15,forward=True)
   # plt.savefig(figures + 'matrix.png')
   
    # Generate random features and distance matrix.
    x = len(labels)
    D = scipy.zeros([x,x])
    for i in range(x):
        for j in range(x):
            for k in range(x):                    
                D[i,j] += (vectors[i][k] - vectors[j][k])**2
            D[i,j] = math.sqrt(D[i,j])
    
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
    fig.savefig(figures + 'dendrogram.png')