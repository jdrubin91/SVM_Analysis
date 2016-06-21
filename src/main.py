__author__ = 'Jonathan Rubin'

import os
#import clean_directory
#import create_intersects
#import create_arrays
#import generate_xy
#import SVM
import intersect_replicates
import create_SVM_files

bidirectional = '/scratch/Shares/dowell/ENCODE/SVM/HCT116/SRR1105737-1_divergent_classifications.bed'
TF = '/scratch/Shares/dowell/ENCODE/K562_TFS/'
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


#def run():
#    for TFfile in os.listdir(TF):
#        if 'cut.sorted' in TFfile:
#            print TFfile
#            clean_directory.run(mapped)
#            create_intersects.run(histones,bidirectional,TF+TFfile,mapped)
#            create_arrays.run(mapped,bidirectional,temp)
#            print "Generating X,Y ..."
#            X,Y,feature_names = generate_xy.run(temp)
#            #print "done\nRunning recursive feature elimination ..."
#            #SVM.recursive_feature_elimination(X,Y,figures)
#            print "done\nRunning univariate feature selection ..."
#            SVM.univariate_feature_selection(X,Y,feature_names,figures,TFfile)
#            print "done"
def run():
    intersect_replicates.run(TF,temp)
    create_SVM_files.run(temp,files)