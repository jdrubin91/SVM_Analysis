__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os

if __name__ == "__main__":
    bidirectional = '/scratch/Shares/dowell/EMG_out_files/human/SRR1552480-1_divergent_classifications.bed'
    TF = '/scratch/Shares/dowell/ENCODE/old/TF_CT/k562/temp/'
    savedir = '/scratch/Users/joru1876/'
    a = pybt.BedTool(bidirectional)
    trackname = list()
    for file1 in os.listdir(TF):
        trackname.append(file1.split('.')[0])
        b = pybt.BedTool(TF + file1)
        a = a.intersect(b,c=True)
        
    a.saveas(savedir + bidirectional.split('/')[-1],trackline='\t'.join(trackname))