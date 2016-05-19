__author__ = 'Jonathan Rubin'

import os

def run(histones,bidirectional,TF,mapped):
    histonelist = list()
    for file1 in os.listdir(histones):
        if 'mp' in file1 and 'tdf' not in file1:
            histonelist.append(histones + file1)

    for item in histonelist:
        os.system("bedtools map -c 4 -a " + TF + " -b " + item + " > " + mapped + item.split('/')[-1])
    
    os.system("bedtools intersect -a " + TF + " -b " + bidirectional + " > " + mapped + bidirectional.split('/')[-1])
