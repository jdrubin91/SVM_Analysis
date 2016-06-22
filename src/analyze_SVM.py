__author__ = 'Jonathan Rubin'

import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt

def run(files='/home/Jonathan/SVM_Analysis/files/',figures='/home/Jonathan/SVM_Analysis/figures/'):
    outfile = open(figures + 'TFs.txt','w')
    for file1 in os.listdir(files):
        TFs = list()
        hist = list()
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
                        if int(line[i]) == 0:
                            zero[i] += 1
                else:
                    pos += 1.0
                    for i in range(len(line[1:])):
                        i = i+1
                        if int(line[i]) != 0:
                            one[i] += 1
        
        for i in range(len(one)):
            S = ((float(one[i])/pos) + (float(zero[i])/neg))/2
            TFs.append((names[i],S))
        hist = [x[1] for x in TFs]
        TFs.sort(key=lambda x: x[1], reverse=True)
        
        
        outfile.write(file1.split('.')[0] + '\t')
        for item in TFs:
            outfile.write(str(item))
        outfile.write('\n')
        
        colLabels=("TF","S-Score")
        nrows, ncols = len(TFs)+1, len(TFs)
        hcell, wcell = 0.3, 1.
        hpad, wpad = 0, 0    
        F1=plt.figure(figsize=(ncols*wcell+wpad, nrows*hcell+hpad))
        ax1 = F1.add_subplot(121)
        ax1.hist(hist,50)
        ax = F1.add_subplot(122)
        ax.axis('off')
        #do the table
        the_table = ax.table(cellText=TFs,colLabels=colLabels,loc='center')
        plt.savefig("table.png")
        
       
if __name__ == "__main__":
    files='C:/cygwin64/home/Jonathan/SVM_Analysis/files/'
    figures='C:/cygwin64/home/Jonathan/SVM_Analysis/figures/'
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
                        if int(line[i]) == 0:
                            zero[i] += 1
                else:
                    pos += 1.0
                    for i in range(len(line[1:])):
                        i = i+1
                        if int(line[i]) != 0:
                            one[i] += 1
        
        for i in range(len(one)):
            S = ((float(one[i])/pos) + (float(zero[i])/neg))/2
            TFs.append((names[i],S))
        print pos
        print neg
        print one
        print zero
        hist = [x[1] for x in TFs]
        TFs.sort(key=lambda x: x[1], reverse=True)
        
        #Histogram of TRCA - TRDMSO
        F1 = plt.figure()
        #plt.title(file1.split('.')[0])
        ax1 = F1.add_subplot(121)
        ax1.hist(hist,50)
        ax2 = F1.add_subplot(122)
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        colLabels=("TF","S-Score")
        the_table = ax2.table(cellText=TFs[0:27], colLabels=colLabels,loc='center',fontsize=1)
        plt.savefig(figures + file1.split('.')[0] + '.png')
        plt.close()