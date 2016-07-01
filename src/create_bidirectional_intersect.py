__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os


def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir
    
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

if __name__ == "__main__":
    homedir = os.path.dirname(os.path.realpath(__file__))
    files = ['/scratch/Users/joru1876/ENCFF001UWQ.bed','/scratch/Shares/dowell/EMG_out_files/human/SRR1552480-1_divergent_classifications.bed']
    temp = '/scratch/Shares/dowell/ENCODE/HOCOMOCODatabaseFIMO/FIMO_OUT_v10/'
    savedir = '/scratch/Users/joru1876/files/'
    for bidirectional in files:
        print bidirectional
        a = pybt.BedTool(bidirectional).cut([0,1,2])
        a.saveas(savedir + bidirectional.split('/')[-1],trackline='Chr\tStart\tStop')
        for folder in os.listdir(temp):
            print folder
            a = pybt.BedTool(bidirectional).cut([0,1,2])
            file1 = temp + folder + '/fimo.bed'
            b = pybt.BedTool(file1).sort()
            a = a.intersect(b,c=True)
            a.saveas(savedir + 'temp.bed',trackline=file1.split('/')[-2].split('_')[0])
            append(savedir + bidirectional.split('/')[-1],savedir + 'temp.bed')
        
    files = ['/scratch/Users/joru1876/ENCFF001UWQ.bed','/scratch/Shares/dowell/EMG_out_files/human/SRR1552480-1_divergent_classifications.bed']
    motif = '/scratch/Shares/dowell/ENCODE/HOCOMOCODatabaseFIMO/FIMO_OUT_v10/'
    temp = parent_dir(homedir) + '/temp/'
    savedir = '/scratch/Users/joru1876/files/'
    
    for bed in files:
        print bed
        a = pybt.BedTool(bed).cut([0,1,2])
        a.saveas(savedir + bed.split('/')[-1],trackline='Chr\tStart\tStop')
        trackname = list()
        for file1 in os.listdir(temp):
            if 'eGFP' not in file1:
                print file1
                for folder in motif:
                    if folder.split('_')[0] == file1:
                        print folder
                        name = file1.split('.')[0]
                        trackname.append(name)
                        trackname.append(name + '_M')
                        a = pybt.BedTool(bed).cut([0,1,2])
                        b = pybt.BedTool(temp + file1).cut([0,1,2]).sort()
                        a = a.intersect(b,c=True)
                        a.saveas(savedir + 'temp.bed',trackline=name)
                        append(savedir + bed.split('/')[-1],savedir + 'temp.bed')
                        a = a = pybt.BedTool(bed).cut([0,1,2])
                        c = pybt.BedTool(motif + folder + '/fimo.bed').cut([0,1,2]).sort()
                        a = a.intersect(c,c=True)
                        a.saveas(savedir + 'temp.bed',trackline=name+'_M')
                        append(savedir + bed.split('/')[-1],savedir + 'temp.bed')
                    
                    
            