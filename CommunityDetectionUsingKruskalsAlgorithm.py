import operator
from igraph import *
import igraph

import Queue as queue

from unionfind import unionfind
from random import randint



#
#       Visual style
#
visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_color"] = "#ff3563"
visual_style["vertex_size"] = 18
visual_style["vertex_label_size"] = 10
visual_style["vertex_label_color"] = "#ffffff"
visual_style["bbox"] = (700, 600)

visual_style1 = {}
visual_style1["edge_curved"] = False
visual_style1["vertex_size"] = 18
visual_style1["vertex_label_size"] = 10
visual_style1["vertex_label_color"] = "#ffffff"
visual_style1["bbox"] = (700, 600)
#visual_style["layout"] = igraph.Graph.layout_random(dim=2)

#
#        Read a graph
#
g = igraph.Graph.Read_GraphML('karate.GraphML')
x = 25
#g = igraph.Graph.Erdos_Renyi(n=x, p=0.2, directed=False, loops=False)
g.vs["label"] = range(1000)
"""
for edge in g.es():
    w = randint(1, 15)
    edge["weight"] = w
    edge["label"] = w
"""    
plot(g, "originalGraph.png", **visual_style)
#print summary(g)

louvainCommunity = g.community_multilevel()
plot(louvainCommunity, "louvain community.png", **visual_style)
print louvainCommunity

girvanNewmanCommunity = g.community_edge_betweenness().as_clustering()
plot(girvanNewmanCommunity, "girvan-newman community.png", **visual_style)

mst = g.copy()
mst.delete_edges(mst.es())

"""
Running kruskal's algorithm
"""

priotrityQ = queue.PriorityQueue()
unionDS = unionfind(g.vcount())

for edge in g.es():
    #print type(edge)
    #weight = edge["weight"]
    priotrityQ.put(edge)
    
while not priotrityQ.empty():
    edge = priotrityQ.get()
    #print edge
    if(unionDS.find(edge.source) != unionDS.find(edge.target)):
        unionDS.unite(edge.source, edge.target)
        mst.add_edges([(edge.source, edge.target)])
     
#print summary(mst)   
plot(mst, "MST.png", **visual_style)

"""
calculating edge betweenness
"""
ebList = mst.edge_betweenness()
ebList = sorted(ebList, key=float, reverse=True)

mst1 = mst.copy()
"""
Approximation of value of k
"""
count = 0
while count < 16:
    k = randint(1,mst.ecount()-1)
    print "************************************************", k
    mst = mst1.copy()
    """
    Removing k-1 edges
    """
    i = 0
    while i < k-1:
        tupleId=0
        for idx, eb in enumerate(ebList):
            if(ebList[i] == eb):
                tupleId = idx;
                break; 
        #if(mst.are_connected(mst.es[tupleId].tuple[0], mst.es[tupleId].tuple[1])):
        if(tupleId < mst.ecount()):
            mst.delete_edges([(mst.es[tupleId].tuple[0], mst.es[tupleId].tuple[1])])
        i+= 1
    plot(mst, "community with k=%d.png"%k, **visual_style)
    comm = mst.clusters(mode=STRONG)
    print comm
    print mst.modularity(comm, weights=None)
    count += 1


    


