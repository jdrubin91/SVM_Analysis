__author__ = 'Jonathan Rubin'

import os

def run(mapped,bidirectional,temp):
    Y = list()
    i = 0
    with open(mapped + bidirectional.split('/')[-1]) as F:
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
    for file1 in os.listdir(mapped):
        if not bidirectional.split('/')[-1] in file1:
            print file1
            feature_names.append(file1)
            l = 0
            with open(mapped + file1) as F:
                for line in F:
                    X[l].append(float(line.strip().split()[-1]))
                    l += 1
    
    print X[0:5]
    outfile = open(temp + 'temp.txt','w')
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