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
    temp = parent_dir(homedir) + '/temp/'
    savedir = '/scratch/Users/joru1876/'
    a = pybt.BedTool(bidirectional).cut([0,1,2])
    trackname = list()
    for file1 in os.listdir(temp):
        trackname.append(file1.split('.')[0])
        b = pybt.BedTool(temp + file1)
        a = a.intersect(b,c=True)
        
    a.saveas(savedir + bidirectional.split('/')[-1],trackline='\t'.join(trackname))