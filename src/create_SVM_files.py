__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os

def run(temp,files,bidirectional,dnase):
    for file1 in os.listdir(temp):
        if 'eGFP' not in file1:
            a = pybt.BedTool(temp + file1).cut([0,1,2]).sort()
            trackname = ['Bidirectional','DNase']
            a = a.intersect(pybt.BedTool(bidirectional).cut([0,1,2]).sort(),wao=True)
            a = a.intersect(pybt.BedTool(dnase).cut([0,1,2]).sort(),wao=True)
            a.saveas(files+file1, trackline='\t'.join(trackname))
            for file2 in os.listdir(temp):
                if file1 != file2 and 'eGFP' not in file2:
                    a = pybt.BedTool(files+file1)
                    print file2
                    trackname.append(file2.split('.')[0])
                    b = pybt.BedTool(temp + file2).cut([0,1,2]).sort()
                    try:
                        a = a.intersect(b,wao=True)
                    except pybt.helpers.BEDToolsError:
                        print "error in: ",file2
                    a.saveas(files + file1,trackline='\t'.join(trackname))