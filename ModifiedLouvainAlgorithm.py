from igraph import *
import queue as queue

"""
        Functions
"""
def getEdgeWithSmallestEdgeBetweennessRatio(g, listOfEdgesAlreadyConsidered):
    "This function calculates edge betweenness ratio of all edges present in graph g"
    #print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    s = "["
    for edge in g.es():
        s = s + "(%d,%d)," % (edge.source, edge.target)
    s = s + "]"
    #print(s)
    edgeBetweennessList = g.edge_betweenness()
    #print(edgeBetweennessList)

    minEdgeBetweenness = max(edgeBetweennessList)
    for eb in edgeBetweennessList:
        if eb < minEdgeBetweenness and eb != 0.0:
            minEdgeBetweenness = eb

    edgeList = []

    for index, edgeBetweenness in enumerate(edgeBetweennessList):
        e = g.es[index]
        if(edgeBetweenness == minEdgeBetweenness and
           e.index not in listOfEdgesAlreadyConsidered and
           e.source != e.target):
            edgeList.append(e)
    return edgeList


def getConnectedComponentUsingBFS(g, vertex):
    "This function finds a connected component starting this vertex using Breadth-First search algorithm and returns it"
    VisitedVertices = []
    q = queue.Queue()

    q.put(vertex)
    VisitedVertices.append(vertex)

    while not q.empty():
        v = q.get()
        #print(type(v),"---", v, "---", g.neighbors(v))

        for v1 in g.neighbors(v):
            vrtx = g.vs[v1]
            #print(":::::::::::::::",type(vrtx))
            if vrtx not in VisitedVertices:
                VisitedVertices.append(vrtx)
                q.put(vrtx)

    return VisitedVertices


def getAllConnectedComponents(g, vCount):
    "This function finds out all connected components of the given graph and returns VertexClustering object"
    Components = []
    VerticesTraversed = []
    VerticesNotTraversed = []

    for index in range (0, g.vcount()):
        VerticesNotTraversed.append(g.vs[index])

    while len(VerticesTraversed) < g.vcount():
        v = VerticesNotTraversed[0]
        s = getConnectedComponentUsingBFS(g, v)

        for vertex in s:
            VerticesNotTraversed.remove(vertex)
            VerticesTraversed.append(vertex)
        Components.append(s)

    #print(Components)
    return Components

def getVertexClusteringFromConnectedComponents(graph, connectedComponents):
    "This function takes connected compoenents and cretaes vertex clustering object"
    membership = []
    for component in connectedComponents:
        if(len(component) == 1):
            index = component[0].index
            membership.insert(index, index)
        else:
            temp = []
            for vertex in component:
                temp.append(vertex.index)
            value = min(temp)
            for vertex in component:
                membership.insert(vertex.index, value)
    #print(membership)
    vertexCluster = VertexClustering(graph, membership=membership)
    return vertexCluster

def getActualVertices(graph, membership, edge, listOfEdgesAlreadyConsidered):
    "This method takes connected components from previous step and returns actual vertices that should be connected"
    tuple = []

    flag = False
    for index1, m1 in enumerate(membership):
       if m1 == edge.source:
           for index2, m2 in enumerate(membership):
               if m2 == edge.target:
                   if graph.are_connected(index1, index2) and graph.get_eid(index1,index2) not in listOfEdgesAlreadyConsidered and edge.index == graph.get_eid(index1, index2):
                        source = index1
                        target = index2
                        flag = True
                        break
       if(flag):
            break
    tuple.append(source)
    tuple.append(target)
    #print("New source and target -- ",tuple)
    return tuple



"""
        Visual styles
"""
visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_color"] = "#ff3563"
visual_style["vertex_size"] = 18
visual_style["vertex_label_size"] = 10
visual_style["vertex_label_color"] = "#ffffff"
visual_style["bbox"] = (700, 600)

"""
         Read a graph
"""
inputGraph = Graph.Barabasi(n = 8, m = 2, zero_appeal=3)
#inputGraph = Graph.Erdos_Renyi(n=25, p=0.08, directed=False, loops=False)
#g = igraph.Graph.Read_GraphML('karate.GraphML')

inputGraph.vs["label"] = range(1000)
noOfVertices = inputGraph.vcount()

plot(inputGraph, "inputGraph.png", **visual_style)

outputGraph = inputGraph.copy()
copyGraph = inputGraph.copy()
outputGraph.delete_edges(outputGraph.es())

"""
        Existing community detection algorithms: Louvain & Girvan-Newman
"""
louvainCommunity = inputGraph.community_multilevel()
plot(louvainCommunity, "louvain community.png", mark_groups=True)
#print louvainCommunity

girvanNewmanCommunity = inputGraph.community_edge_betweenness().as_clustering()
plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)

isLocalMaximaAchievedCount = 3;
maxModularity = -1;
maxModularityCommunities = []
listOfEdgesAlreadyConsidered = []
idx = 1;
connectedComponents = getAllConnectedComponents(outputGraph, noOfVertices)
vertexCluster = getVertexClusteringFromConnectedComponents(outputGraph, connectedComponents)

while isLocalMaximaAchievedCount >= 0:
    edgeList = getEdgeWithSmallestEdgeBetweennessRatio(inputGraph, listOfEdgesAlreadyConsidered)

    for edge in edgeList:
        #print(edge.tuple)
        tuples = getActualVertices(copyGraph, vertexCluster.membership, edge, listOfEdgesAlreadyConsidered)
        listOfEdgesAlreadyConsidered.append(edge.index)
        source = tuples[0]
        target = tuples[1]
        outputGraph.add_edges([(source, target)])

    connectedComponents = getAllConnectedComponents(outputGraph, noOfVertices)
    vertexCluster = getVertexClusteringFromConnectedComponents(outputGraph, connectedComponents)
    #componentList = outputGraph.clusters(mode="STRONG")

    inputGraph = copyGraph.copy()
    inputGraph.contract_vertices(vertexCluster.membership, combine_attrs=min(vertexCluster.membership))

    modularity = vertexCluster.recalculate_modularity()
    if(maxModularity < modularity):
        maxModularity = modularity
        isLocalMaximaAchievedCount = 3;
    else:
        isLocalMaximaAchievedCount = 1

    print("%d   Modularity = %f" %(idx,modularity))
    plot(outputGraph, "outputGraph%d.png" %idx, **visual_style)
    idx += 1