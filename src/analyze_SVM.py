__author__ = 'Jonathan Rubin'

import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt
import scipy.stats as stats

def run(files,figures):
    outfile = open(figures + 'TFs.txt','w')
    for file1 in os.listdir(files):
        print file1
        TFs = list()
        hist = list()
        pos = 0
        neg = 0
        with open(files + file1) as F:
            names = F.readline().strip().split()[1:]
            one = [0] * len(names)
            zero = [0] * len(names)
            alist = [0] * len(names)
            blist = [0] * len(names)
            clist = [0] * len(names)
            dlist = [0] * len(names)
            for line in F:
                line = line.strip().split()[3:]
                for i in range(len(line[1:])):
                    if int(line[i+1]) > 0:
                        alist[i] += 1.0
                    else:
                        blist[i] += 1.0
                if line[0] == '0':
                    neg += 1.0
                    for i in range(len(line[1:])):
                        if int(line[i+1]) == 0:
                            zero[i] += 1.0
                        else:
                            clist[i] += 1.0
                else:
                    pos += 1.0
                    for i in range(len(line[1:])):
                        if int(line[i+1]) != 0:
                            one[i] += 1.0
                        else:
                            dlist[i] += 1.0
        
        for i in range(len(one)):
            N = pos + neg
            p = pos/N
            a = alist[i]/N
            #S = one[i] - N*p*a
            S = 1.0-stats.binom(N,p*a).cdf(one[i])
            S2 = stats.binom(N,p*(1-a)).cdf(dlist[i])
            S3 = stats.binom(N,(1-p)*a).cdf(clist[i])
            S4 = 1.0-stats.binom(N,(1-p)*(1-a)).cdf(zero[i])
            #print alist[i], one[i],zero[i],pos,neg,N
            if alist[i] == 0:
                alist[i] = 0.002
                one[i] += 0.001
            if blist[i] == 0:
                blist[i] = 0.002
                zero[i] += 0.001
                
            S5 = ((float(one[i])/alist[i]) + (float(zero[i])/blist[i]))/2
            TFs.append((names[i],S,S2,S3,S4,S5))
        hist = [x[1] for x in TFs]
        TFs.sort(key=lambda x: x[5], reverse=True)
        outfile.write(file1.split('.')[0] + '\t')
        for item in TFs:
            for val in item:
                outfile.write(str(val) + ",")
        outfile.write('\n')
        
        #F1 = plt.figure()
        #ax1 = F1.add_subplot(121)
        #ax1.hist(hist,50)
        #ax2 = F1.add_subplot(122)
        #ax2.xaxis.set_visible(False)
        #ax2.yaxis.set_visible(False)
        #colLabels=("TF","p-value","S-Score")
        #the_table = ax2.table(cellText=TFs[:27], colLabels=colLabels, loc='center',fontsize=1)
        #plt.savefig(figures + file1.split('.')[0] + '.png')
        #plt.close()
        
    outfile.close()
        
       
