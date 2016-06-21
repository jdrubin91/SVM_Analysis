__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os

def run(temp,files,bidirectional):
    for file1 in os.listdir(temp):
        print "TF: ",file1
        a = pybt.BedTool(temp + file1)
        trackname = ['Bidirectional']
        a = a.intersect(pybt.BedTool(bidirectional),c=True)
        for file2 in os.listdir(temp):
            if file1 not in file2:
                trackname.append(file2.split('.')[0])
                b = pybt.BedTool(temp + file2)
                a = a.intersect(b,c=True)
        a.saveas(files + file1,trackline='\t'.join(trackname))