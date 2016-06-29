__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os


def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

if __name__ == "__main__":
    homedir = os.path.dirname(os.path.realpath(__file__))
    bidirectional = '/scratch/Users/joru1876/ENCFF001UWQ.bed'
    temp = '/scratch/Shares/dowell/ENCODE/HOCOMOCODatabaseFIMO/FIMO_OUT_v10/'
    savedir = '/scratch/Users/joru1876/files/'
    a = pybt.BedTool(bidirectional).cut([0,1,2])
    trackname = list()
    for folder in os.listdir(temp):
        print folder
        file1 = temp + folder + '/fimo.bed'
        trackname.append(file1.split('.')[0])
        b = pybt.BedTool(temp + file1).sort()
        a = a.intersect(b,c=True)
        
    a.saveas(savedir + bidirectional.split('/')[-1],trackline='\t'.join(trackname))
    
    
    bidirectional = '/scratch/Shares/dowell/EMG_out_files/human/SRR1552480-1_divergent_classifications.bed'
    temp = '/scratch/Shares/dowell/ENCODE/HOCOMOCODatabaseFIMO/FIMO_OUT_v10/'
    savedir = '/scratch/Users/joru1876/files/'
    a = pybt.BedTool(bidirectional).cut([0,1,2])
    trackname = list()
    for folder in os.listdir(temp):
        print folder
        file1 = temp + folder + '/fimo.bed'
        trackname.append(file1.split('.')[0])
        b = pybt.BedTool(temp + file1).sort()
        a = a.intersect(b,c=True)
        
    a.saveas(savedir + bidirectional.split('/')[-1],trackline='\t'.join(trackname))