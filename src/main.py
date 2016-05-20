__author__ = 'Jonathan Rubin'

import os
import create_intersects
import create_arrays
import generate_xy
import SVM

bidirectional = '/scratch/Shares/dowell/ENCODE/SVM/HCT116/SRR1105737-1_divergent_classifications.bed'
TF = '/scratch/Shares/dowell/ENCODE/SVM/HCT116/TF_ChIP/SRF-human.bed.cut'
histones = '/scratch/Shares/dowell/ENCODE/SVM/HCT116/histone_mods/bowtie2/sortedbam/genomecoveragebed/fortdf/'



#Return parent directory
def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

#Home directory
homedir = os.path.dirname(os.path.realpath(__file__))

#Files directory
files = parent_dir(homedir) + '/files/'

#Mapped directory
mapped = parent_dir(homedir) + '/mapped/'

#Temp directory
temp = parent_dir(homedir) + '/temp/'

#Figure directory
figures = parent_dir(homedir) + '/figures/'


def run():
    #create_intersects.run(histones,bidirectional,TF,mapped)
    #create_arrays.run(mapped,bidirectional,temp)
    X,Y,feature_names = generate_xy.run(temp)
    #SVM.recursive_feature_elimination(X,Y,figures)
    SVM.univariate_feature_selection(X,Y,feature_names,figures)
    