import operator
from igraph import *
import queue as queue

from unionfind import unionfind
from random import randint

"""
        Functions
"""
def calculateWeightOfEdgeUsingNeighborhoodOverlap(graph, edge):
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

    if((degreeA + degreeB - 2) == 0):
        NP = 0
    else:
        NP = commonNeighbors / (degreeA + degreeB - 2)

    return NP

def calculateWeightOfEdgeUsingDegree(graph, edge):
    "This method calculates the weight of the edge using degree of its endpoints"
    weight = len(graph.neighbors(edge.source)) + len(graph.neighbors(edge.target))
    return weight

"""
        Visual Style
"""
visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_color"] = "#13a53f"
visual_style["vertex_size"] = 16
visual_style["vertex_label_size"] = 12
visual_style["vertex_label_color"] = "#ffffff"
visual_style["bbox"] = (300, 230)

"""
        Input graph
"""
x = 18
#inputGraph = Graph.Read_GraphML('karate.GraphML')
#inputGraph = Graph.Read_Edgelist('0.edges',directed=False)
#inputGraph = read('football.gml')
#inputGraph = read('dolphins.gml')
inputGraph = Graph.Barabasi(n=x, m=3, zero_appeal=3)
print(summary(inputGraph))

#inputGraph.vs["label"] = range(1000)
for v in inputGraph.vs():
    v['label'] = v.index

for edge in inputGraph.es():
    #weight = calculateWeightOfEdgeUsingNeighborhoodOverlap(inputGraph, edge)
    weight = calculateWeightOfEdgeUsingDegree(inputGraph, edge)
    edge["weight"] = weight
    #edge['label'] = NP

plot(inputGraph, "graph01.png", **visual_style)
#print summary(g)

"""
        Existing community detection algorithms: Louvain & Girvan-Newman
"""
louvainCommunity = inputGraph.community_multilevel()
plot(louvainCommunity, "louvain community.png", mark_groups=True)
print("\n************************* LOUVAIN ALGORITHM *************************")
print(summary(louvainCommunity))
print("Modularity of Louvain algorithm = %f\t\t"%louvainCommunity.q,"\n\n")

girvanNewmanCommunity = inputGraph.community_edge_betweenness().as_clustering()
plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)
print("************************* GIRVAN-NEWMAN ALGORITHM ********************")
print(summary(girvanNewmanCommunity))
print("Modularity of Girvan-Newman algorithm = %f"%girvanNewmanCommunity.q,"\n\n\n")

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
index = 0
maxModularity = -1

while count < 20:

    while len(alreadyUsedValuesOfK) != mst.ecount():
        k = randint(1, mst.ecount())
        if k not in alreadyUsedValuesOfK:
            alreadyUsedValuesOfK.append(k)
            break
    print ("************************************************  k = ", k)
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

    modularity = comm.q
    if (maxModularity < modularity):
        maxModularity = modularity
        index = k
        maxModularityCommunities = comm

    print(summary(comm))
    print("Modularity = %f\t\t" % (comm.q))
    # print("%d   Modularity with igraph  method = %f\t\t" % (idx, componentList.q),summary(vertexCluster))
    plot(comm, "outputGraph%d.png" %k, mark_groups=True)
    count += 1


print("\n\nMax modularity index = %d"%index)
print("Number of communities  =  ", len(set(maxModularityCommunities.membership)))
print("Modularity = %f\t\t" % (maxModularity))
plot(maxModularityCommunities, "outputGraph.png", mark_groups=True)
exit()

    


