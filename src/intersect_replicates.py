__author__ = 'Jonathan Rubin'

import os
import pybedtools as pybt

def run(directory,temp):
    for folder in os.listdir(directory):
        replicates = list()
        for file1 in os.listdir(directory + folder):
            if 'peaks.bed' in file1:
                replicates.append(directory + folder + '/' + file1)
        a = pybt.BedTool(replicates[0])
        for i in range(len(replicates)-1):
            a = a.intersect(pybt.BedTool(replicates[i+1]))
        outfile = open(temp + folder + '.bed','w')
        outfile.write(a)
        