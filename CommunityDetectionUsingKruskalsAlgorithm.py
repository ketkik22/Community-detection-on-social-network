import operator
from igraph import *
import queue as queue

from unionfind import unionfind
from random import randint

"""
        Functions
"""
def calculateNeighborhoodOverlap(graph, edge):
    "This fucntion will calculate the neighborhood overlap of an edge and return it"
    NP = 0

    neighborsA = graph.neighbors(edge.source)
    neighborsB = graph.neighbors(edge.target)

    commonNeighbors = 0

    if  len(neighborsA) < len(neighborsB):
        for vertex in neighborsA:
            if vertex in neighborsB:
                commonNeighbors += 1
    else:
        for vertex in neighborsB:
            if vertex in neighborsA:
                commonNeighbors += 1

    degreeA = graph.degree(edge.source,loops=False)
    degreeB = graph.degree(edge.target,loops=False)

    NP = commonNeighbors / (degreeA + degreeB - 2)

    return NP

"""
        Visual Style
"""
visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_color"] = "#ff3563"
visual_style["vertex_size"] = 18
visual_style["vertex_label_size"] = 10
visual_style["vertex_label_color"] = "#ffffff"
visual_style["bbox"] = (700, 600)

"""
        Input graph
"""
x = 40
#inputGraph = Graph.Read_GraphML('karate.GraphML')
inputGraph = Graph.Read_Edgelist('0.edges',directed=False)
#inputGraph = Graph.Barabasi(n=x, m=2, zero_appeal=3)
inputGraph.vs["label"] = range(1000)

for edge in inputGraph.es():
    NP = calculateNeighborhoodOverlap(inputGraph, edge)
    edge["weight"] = NP
    #edge['label'] = NP

plot(inputGraph, "originalGraph.png", **visual_style)
#print summary(g)

louvainCommunity = inputGraph.community_multilevel()
plot(louvainCommunity, "louvain community.png", mark_groups=True)
print("Louvain algorithm")
print(summary(louvainCommunity))
print(louvainCommunity.q)

girvanNewmanCommunity = inputGraph.community_edge_betweenness().as_clustering()
plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)
print("Girvan-Newman algorithm ")
print(summary(girvanNewmanCommunity))
print(girvanNewmanCommunity.q)
print("\n\n")

mstTree = Graph.spanning_tree(inputGraph, weights=inputGraph.es['weight'], return_tree=True)
plot(mstTree, "spanningTreeByPrim.png", **visual_style)

mst = inputGraph.copy()
mst.delete_edges(mst.es())

"""
Running kruskal's algorithm
"""

priotrityQWeights = queue.PriorityQueue()
unionDS = unionfind(inputGraph.vcount())
alreadyUsedEdges = []

for edge in inputGraph.es():
    #print(type(edge))
    weight = edge["weight"]
    priotrityQWeights.put(weight)
    #print(edge.tuple, "-------", edge['weight'])
    
while not priotrityQWeights.empty():
    weight = priotrityQWeights.get()
    #print(priotrityQWeights.qsize())

    for e in inputGraph.es():
        if (e['weight'] == weight and e not in alreadyUsedEdges):
            edge = e
            alreadyUsedEdges.append(edge)
            break
    #print(edge.tuple, "-------", edge['weight'])

    if(unionDS.find(edge.source) != unionDS.find(edge.target)):
        unionDS.unite(edge.source, edge.target)
        mst.add_edges([(edge.source, edge.target)])

plot(mst, "MST.png", **visual_style)

"""
calculating edge betweenness
"""
ebList = mst.edge_betweenness()
alreadyUsedValuesOfK = []
mst1 = mst.copy()
"""
Approximation of value of k
"""
count = 0
while count < 20:

    while len(alreadyUsedValuesOfK) != mst.ecount():
        k = randint(1, mst.ecount())
        if k not in alreadyUsedValuesOfK:
            alreadyUsedValuesOfK.append(k)
            break
    print ("************************************************", k)
    mst = mst1.copy()
    ebList = mst.edge_betweenness()

    """
    Removing k-1 edges
    """
    i = 0
    while i < k-1:
        tupleId=0
        maxEdgeBetweenness = max(ebList)
        for idx, eb in enumerate(ebList):
            if(maxEdgeBetweenness == eb):
                tupleId = idx;
                break;
        #if(mst.are_connected(mst.es[tupleId].tuple[0], mst.es[tupleId].tuple[1])):
        if(tupleId < mst.ecount()):
            mst.delete_edges([(mst.es[tupleId].tuple[0], mst.es[tupleId].tuple[1])])
            ebList.remove(maxEdgeBetweenness)
        i+= 1

    comm = mst.clusters(mode="STRONG")
    plot(comm, "community with k=%d.png"%k, mark_groups=True)

    #print(comm)
    print(mst.modularity(comm))
    count += 1

exit()

    


