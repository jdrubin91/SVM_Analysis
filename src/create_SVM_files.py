__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os

def run(temp,files,bidirectional,dnase):
    for file1 in os.listdir(temp):
        a = pybt.BedTool(temp + file1)
        trackname = ['Bidirectional','DNase']
        a = a.intersect(pybt.BedTool(bidirectional),wao=True)
        a = a.intersect(pybt.BedTool(dnase),wao=True)
        for file2 in os.listdir(temp):
            if file1 != file2:
                trackname.append(file2.split('.')[0])
                b = pybt.BedTool(temp + file2)
                a = a.intersect(b,wao=True)
                
        print file1, len(trackname)
        a.saveas(files + file1,trackline='\t'.join(trackname))