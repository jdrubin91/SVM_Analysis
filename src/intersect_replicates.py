__author__ = 'Jonathan Rubin'

import os
import pybedtools as pybt

def run(directory,temp):
    for folder in os.listdir(directory):
        if len(os.listdir(directory + folder)) > 1:
            replicates = list()
            for file1 in os.listdir(directory + folder):
                replicates.append(directory + folder + '/' + file1)
            a = pybt.BedTool(replicates[0]).cut([0,1,2])
            a.sort()
            for i in range(len(replicates)-1):
                a = a.intersect(pybt.BedTool(replicates[i+1]).sort())
            a.saveas(temp + folder + '.bed')
        else:
            for file1 in os.listdir(directory + folder):
                a = pybt.BedTool(directory + folder + '/' + file1).cut([0,1,2])
                a.saveas(temp + folder + '.bed')
                
        