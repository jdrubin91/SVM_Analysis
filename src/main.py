__author__ = 'Jonathan Rubin'

import os
#import clean_directory
#import create_intersects
#import create_arrays
#import generate_xy
#import SVM
import intersect_replicates
import create_SVM_files
import analyze_SVM
import create_network
import create_boxplot
import create_matrix

bidirectional = '/scratch/Shares/dowell/EMG_out_files/human/SRR1552480-1_divergent_classifications.bed'
dnase = '/scratch/Users/joru1876/ENCFF001UWQ.bed'
#TF = '/scratch/Shares/dowell/ENCODE/K562_TFS/'
TF = '/scratch/Shares/dowell/ENCODE/old/TF_CT/k562/temp/'
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

#This version of main.run() creates support vector files for each TF.  Each file
#is a bed file with all ChIP peaks for a given TF intersected with bidirectionals
#and all other TFs.  An S-Score is calculated by the average of true positive perecentage
#and true negative percentage
def run():
    #print "Intersecting Replicates..."
    #intersect_replicates.run(TF,temp)
    print "done\nCreating SVM files..."
    create_SVM_files.run(temp,files,bidirectional,dnase)
    print "done\nAnalyzing SVs..."
    analyze_SVM.run(files,figures)
    print "done\nCreating Network..."
    create_network.run(figures)
    create_boxplot.run(files,figures)
    create_matrix.run(files,figures)