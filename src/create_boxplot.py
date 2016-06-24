__author__ = 'Jonathan Rubin'

import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt

def run(files,figures):
    pos = list()
    neg = list()
    for file1 in os.listdir(files):
        print file1
        with open(files+file1) as F:
            F.readline()
            for line in F:
                line = line.strip().split()
                weights = [int(i) for i in line[3:]]
                bidirectional = weights[0]
                if sum([1 for i in weights[1:] if i > 0]) > 100:
                    print file1,line[0:3]
                if bidirectional == 0:
                    neg.append(sum([1 for i in weights[1:] if i > 0]))
                else:
                    pos.append(sum([1 for i in weights[1:] if i > 0]))

    F = plt.figure()
    ax1 = F.add_subplot(111)
    bp1 = ax1.boxplot([pos,neg],patch_artist=True)
    ax1.set_xticklabels(['Bidirectional','No Bidirectional'])
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()
    ## change outline color, fill color and linewidth of the boxes
    for box in bp1['boxes']:
        # change outline color
        box.set( color='#7570b3', linewidth=2)
        # change fill color
        box.set( facecolor = '#1b9e77' )
    ## change color and linewidth of the whiskers
    for whisker in bp1['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)
    ## change color and linewidth of the caps
    for cap in bp1['caps']:
        cap.set(color='#7570b3', linewidth=2)
    ## change color and linewidth of the medians
    for median in bp1['medians']:
        median.set(color='#b2df8a', linewidth=2)
    ## change the style of fliers and their fill
    for flier in bp1['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)
    plt.savefig(figures + '/Boxplot.png')