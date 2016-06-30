__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os


def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

if __name__ == "__main__":
    homedir = os.path.dirname(os.path.realpath(__file__))
    files = ['/scratch/Users/joru1876/ENCFF001UWQ.bed','/scratch/Shares/dowell/EMG_out_files/human/SRR1552480-1_divergent_classifications.bed']
    temp = '/scratch/Shares/dowell/ENCODE/HOCOMOCODatabaseFIMO/FIMO_OUT_v10/'
    savedir = '/scratch/Users/joru1876/files/'
    for bidirectional in files:
        a = pybt.BedTool(bidirectional).cut([0,1,2])
        trackname = list()
        for folder in os.listdir(temp):
            print folder
            file1 = temp + folder + '/fimo.bed'
            trackname.append(file1.split('/')[-2].split('_')[0])
            b = pybt.BedTool(file1).sort()
            a = a.intersect(b,c=True)
            
        a.saveas(savedir + bidirectional.split('/')[-1],trackline='\t'.join(trackname))
        
    files = ['/scratch/Users/joru1876/ENCFF001UWQ.bed','/scratch/Shares/dowell/EMG_out_files/human/SRR1552480-1_divergent_classifications.bed']
    motif = '/scratch/Shares/dowell/ENCODE/HOCOMOCODatabaseFIMO/FIMO_OUT_v10/'
    temp = parent_dir(homedir) + '/temp/'
    savedir = '/scratch/Users/joru1876/files/'
    
    for bed in files:
        a = pybt.BedTool(bed).cut([0,1,2])
        trackname = list()
        for file1 in temp:
            print file1
            for folder in motif:
                if folder.split('_')[0] == file1:
                    print folder
                    name = file1.split('.')[0]
                    trackname.append(name)
                    trackname.append(name + '_M')
                    b = pybt.BedTool(temp + file1).cut([0,1,2]).sort()
                    c = pybt.BedTool(motif + folder + '/fimo.bed').cut([0,1,2]).sort()
                    a = a.intersect(b,c=True)
                    a = a.intersect(c,c=True)
                    
        a.saveas(savedir + bed.split('/')[-1],trackline='\t'.join(trackname))
                    
                    
            