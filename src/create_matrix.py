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
        print TFi
        N = S[TFi][0]
        p = S[TFi][1]
        TFs = S[TFi][2]
        weights = S[TFi][3]
        b = S[TFi][4]
        for j in range(len(TFs)):
            TFj = TFs[j]
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
            d1[TFi] = [(TFi,1.0)]
        Si = I[pair]
        Sj = I[TFj + '~' + TFi]
        d1[TFi].append((TFj,(Si+Sj)/2.0))
    
    order = list()
    for key in d1:
        i = 0
        for tuple1 in d1[key]:
            i += tuple1[1]
        order.append((key,i))
    
    order = sorted(order,key=itemgetter(1),reverse=True)
    labels = [i for (i,j) in order]
    vectors = [d1[name][i] for name,i in labels,range(len(d1[name]))]
    print vectors
    
    
    vectors = np.array(vectors)
    d = np.zeros((vectors.shape[1],vectors.shape[1]))
    print d.shape
    for i in range(vectors.shape[1]):
        for j in range(vectors.shape[1]):
            d[i,j] = np.sum(np.abs(vectors[:,i]-vectors[:,j]))
    y=linkage(d,method="average")
    z=dendrogram(y,no_plot=True)
    idx=z["leaves"]
    vectors=vectors[:,idx]
            
            
            
    F=plt.figure(figsize=(15,10))
    ax=F.add_axes([0.07,0.1,0.7,0.7])
    
    heatmap = ax.pcolor(vectors, cmap=plt.cm.YlOrBr, alpha=0.8, vmin=-200,vmax=0)
    fig = plt.gcf()
    
    
    # turn off the frame
    ax.set_frame_on(False)
    
    # put the major ticks at the middle of each cell
    res = 7
    ax.set_yticks(np.arange(0,vectors.shape[0],res))
    print len(np.arange(0,vectors.shape[0],res))
    ax.set_xticks(np.arange(vectors.shape[1]) + 0.5, minor=False)
    
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.yaxis.tick_right()
    ax.xaxis.tick_top()
    
    # note I could have used nba_sort.columns but made "labels" instead
    #ax.set_xticklabels(["".join(e.split("bidir")[0].strip('_')) for e in exporder], minor=False,fontsize = 10)
    #ax.set_yticklabels([",".join([ TForder[j] for j in range(i,min(i+res, vectors.shape[0]) ) ]) for i in np.arange(0,vectors.shape[0], res)], minor=False,fontsize = 10)
    
    ax.set_xticklabels(["".join(labels)], minor=False,fontsize = 10)
    ax.set_yticklabels([",".join(labels) for i in np.arange(0,vectors.shape[0], res)], minor=False,fontsize = 10)
    
    # rotate the
    plt.xticks(rotation=90)
    
    ax.grid(False)
    
    # Turn off all the ticks
    ax = plt.gca()
    
    for t in ax.xaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
    for t in ax.yaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
    
    fig.set_size_inches(20, 15,forward=True)
    plt.savefig(figures + 'matrix.png')