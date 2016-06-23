__author__ = 'Jonathan Rubin'

import networkx as nx
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt

def run(figures):
    network = dict()
    with open(figures+"TFs.txt") as F:
        for line in F:
            line = line.strip().split()
            TF = line[0]
            weights = line[1].split(',')
            network[TF] = weights[:-1]
    

    G = nx.Graph()
    for TF in network:
        for i in range(0, (int(len(network[TF])-5)), 6):
            if float(network[TF][i+1]) < 0.01 and float(network[TF][i+2]) < 0.01 and float(network[TF][i+3]) < 0.01 and float(network[TF][i+4]) < 0.01:
                G.add_edge(TF,network[TF][i],weight=0.0001)
        
    
    
    
    edgewidth = [ d['weight'] for (u,v,d) in G.edges(data=True)] 
    #elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.6]       
    
    pos=nx.spring_layout(G)
    plt.figure()
    plt.subplot(111)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color=edgewidth)
    nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')
    plt.savefig(figures+'network.png')