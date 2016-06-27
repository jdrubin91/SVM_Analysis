__author__ = 'Jonathan Rubin'

import os

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
        S[file1] = [N,p,TFs,weights,b]
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
                I[TFi + '~' + TFj] = 0
            else:
                I[TFi + '~' + TFj] = bj/Ex
    
    name = list()
    val = list()
    for pair in I:
        TFi,TFj = pair.split('-')
        if not TFj + '~' + TFi in name:
            name.append(pair)
            Si = I[pair]
            Sj = I[TFj + '~' + TFi]
            val.append((Si+Sj)/2)
    
    print name
    print val
            