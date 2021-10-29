# You have to import push_pop script

from push_pop import *
# %run push_pop.ipynb

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
from numpy import genfromtxt


# DEFINE FUNCTIONS


def E_walk(walker): # Calculate the walker hamiltonian
    abs_walker = abs(walker)
    return -1*sum(walker*abs_walker)


def Metropolis(G,H,walker,new_walker):
    
    E_diff = E_walk(new_walker) - E_walk(walker) # Calculate energy diff for Metropolis
    
    if E_diff <= 0.0000000001: # Tolerance to negate numeric error
        walker = new_walker
        G = H
        
    else:
        Temp = 0.5
        if random.random() < math.exp(-E_diff/Temp):
            walker = new_walker
            G = H
        else:
            pass
        
    return G, walker


def K(G,node): # Find curvature at particular node
    return 6 - G.degree(node)


def draw(G):
    plt.figure(figsize=(3,3))
    nx.draw(G, pos=nx.spring_layout(G), node_color='lightgray', edge_color='black', with_labels=True)
    return


def rename_nodes(G): # rename all node in the graph starting from number zero
    num = 0
    G = nx.convert_node_labels_to_integers(H, first_label = num, ordering='default')
    return G


def get_walker(G, walker, node, new_node):
    
    split = walker[node]//2
    
    walker[node] -= split # Split the walkers between the nodes
    walker[new_node] += split
    
    for i in range(0, max( G.nodes() )+1 ): # Adding walker using the curvature at each node
        walker[i] += K(G,i)
    
    if len(G) > 2:
        listofnodes = [k for k in G] # Get a list of all nodes in the graph G
        for i in range(12):
            walker[random.choice(listofnodes)] -= 1 # Add twelve -1 walkers to random nodes in graph G
 
    new_walker = np.zeros(len(walker)).astype(int)
    
    for i in G.nodes(): # loop through all node to move the walkers
        
        for j in range(0, int(abs(walker[i])) ): # All walker at node i gets to "walk"
            
            nbr = [n for n in G[i]] # Get list of neighbor for node i in G
            k = random.choice(nbr)  # walker will move to neighbor k

            if walker[i] > 0:  # move the walker depending on whether it's a +1 walker or -1
                new_walker[k] += 1
            if walker[i] < 0:
                new_walker[k] -= 1
            if walker[i] == 0:
                continue

    return new_walker # Make sure to pass this back, i.e. walker = get_walker(G,walker)


def reconfigure_walker(G, walker):
    walker2 = np.zeros(len(walker)).astype(int)
    
    j = 0
    for i in G.nodes(): # loop through all node, one should be missing since it "popped".
        walker2[j] = walker[i] # read explanation below
        j += 1

    return walker2

# index i will loop through 0,1,2,.... except for the missing node
# index j will is just 0,1,2,3,....
# let's say node 2 is gone cause it "popped", walker2[0] = walker[0], walker2[1] = walker[1],
# then walker2[2] = walker[3], walker2[3] = walker[4], and so on.

# After running this function, we can then run the "rename_nodes()" function to relabel the nodes 0,1,2,3....









# MAIN CODE START HERE

G = nx.octahedral_graph()

s = 2**8

walker = np.zeros(s).astype(int)

for i in range(0,max(G.nodes())+1): # Adding walker using the curvature at each node
    walker[i] += K(G,i)

while len(G) < s:
    
    H = G.copy()
    new_walker = walker.copy()

    node, new_node = push(H)

    new_walker = get_walker(H, new_walker, node, new_node)
    
    G, walker = Metropolis(G, H, walker, new_walker)
    
    if G == H:
        print("Current number of nodes: ", len(G))


# Equilibration / Thermalizing

for i in range(0,8*s):
    
    H = G.copy()
    pop(H)
    walker = reconfigure_walker(H, walker)
    H = rename_nodes(H)
    push(H)
    
    new_walker = walker.copy()
    new_walker = get_walker(H, new_walker, node, new_node)
    
    G, walker = Metropolis(G, H, walker, new_walker)


a = get_adj(G)
np.savetxt("adjacency.csv", a.astype(int), fmt='%i', delimiter=",")
#np.savetxt("walker_array.csv", walker.astype(int), fmt='%i', delimiter=",")

