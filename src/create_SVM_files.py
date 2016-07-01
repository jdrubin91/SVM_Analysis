__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os

def append(file1,file2):
    linelist = list()
    with open(file1) as F1:
        with open(file2)as F2:
            for line1 in F1:
                line2 = F2.readline()
                add = line2.strip().split()[-1]
                linelist.append(line1.strip() + '\t' + add + '\n')
    
    outfile = open(file1,'w')
    for line in linelist:
        outfile.write(line)

def add_header(file1,header):
    linelist = list()
    with open(file1) as F:
        for line in F:
            linelist.append(line)
            
    outfile = open(file1,'w')
    outfile.write(header)
    for line in linelist:
        outfile.write(line)

def run(temp,files,bidirectional,dnase):
    for file1 in os.listdir(temp):
        if 'eGFP' not in file1:
            a = pybt.BedTool(temp + file1).cut([0,1,2]).sort()
            a.saveas(files+file1)
            print files+file1
            a = pybt.BedTool(files + file1).cut([0,1,2]).sort()
            b = pybt.BedTool(bidirectional).cut([0,1,2]).sort()
            a = a.intersect(b,wao=True)
            a.saveas(files+'temp.bed')
            append(files+file1,files+'temp.bed')
            a = pybt.BedTool(files + file1)
            b = pybt.BedTool(dnase).cut([0,1,2]).sort()
            a = a.intersect(b,wao=True)
            a.saveas(files+'temp.bed')
            append(files+file1,files+'temp.bed')
            header = ['Bidirectional','DNase']
            for file2 in os.listdir(temp):
                if file1 != file2 and 'eGFP' not in file2:
                    a = pybt.BedTool(files+file1)
                    print file2
                    header.append(file2)
                    b = pybt.BedTool(temp + file2).cut([0,1,2]).sort()
                    a = a.intersect(b,wao=True)
                    a.saveas(files+'temp.bed')
                    append(files+file1,files+'temp.bed')
                    
        add_header(files+file1,'\t'.join(header))