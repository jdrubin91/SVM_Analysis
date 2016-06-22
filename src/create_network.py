__author__ = 'Jonathan Rubin'

import networkx as nx
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
            network[TF] = weights
    
    G = nx.Graph()
    for TF in network:
        for i in range(0, len(network[TF]), 2):
            G.add_edge(TF,network[TF][i],weight=float(network[TF][i+1]))
    
    edgewidth = [ d['weight'] for (u,v,d) in G.edges(data=True)]        
    pos=nx.spring_layout(G)
    
    plt.figure(1)
    plt.subplot(211); plt.axis('off')
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, width=edgewidth,)
    plt.savefig(figures+'network.png')