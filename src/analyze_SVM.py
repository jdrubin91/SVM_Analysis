__author__ = 'Jonathan Rubin'

import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt

def run(files,figures):
    hist = list()
    TFs = list()
    for file1 in os.listdir(files):
        print file1
        pos = 0
        neg = 0
        with open(files + file1) as F:
            names = F.readline().strip().split()
            one = [0] * len(names)
            zero = [0] * len(names)
            for line in F:
                line = line.strip().split()[3:]
                if line[0] == '0':
                    neg += 1.0
                    for i in range(len(line[1:])):
                        i = i+1
                        zero[i] += abs(int(line[i])-1)
                else:
                    pos += 1.0
                    for i in range(len(line[1:])):
                        i = i+1
                        one[i] += int(line[i])
        
        for i in range(len(one)):
            S = ((float(one[i])/pos) + (float(zero[i])/neg))/2
            TFs.append((names[i],S))
        hist = [x[1] for x in TFs]
        TFs.sort(key=lambda x: x[1], reverse=True)
        
        #Histogram of TRCA - TRDMSO
        F1 = plt.figure()
        plt.title(file1.split('.')[0])
        ax1 = F1.add_subplot(121)
        ax1.hist(hist,50)
        ax2 = F1.add_subplot(122)
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        colLabels=("TF","S-Score")
        the_table = ax2.table(cellText=TFs, colLabels=colLabels,loc='center',fontsize=8)
        plt.savefig(figures + file1.split('.')[0] + '.png')
        plt.close()