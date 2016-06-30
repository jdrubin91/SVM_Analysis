__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os

def run(temp,files,bidirectional,dnase):
    for file1 in os.listdir(temp):
        a = pybt.BedTool(temp + file1).cut([0,1,2]).sort()
        trackname = ['Bidirectional','DNase']
        a = a.intersect(pybt.BedTool(bidirectional).cut([0,1,2]).sort(),wao=True)
        print "Intersected bidir"
        a = a.intersect(pybt.BedTool(dnase).cut([0,1,2]).sort(),wao=True)
        print "Intersected DNase"
        for file2 in os.listdir(temp):
            if file1 != file2:
                trackname.append(file2.split('.')[0])
                b = pybt.BedTool(temp + file2).cut([0,1,2]).sort()
                a = a.intersect(b,wao=True)
                
        print file1, len(trackname)
        a.saveas(files + file1,trackline='\t'.join(trackname))