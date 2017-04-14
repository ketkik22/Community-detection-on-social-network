from igraph import *
import queue as queue

"""
        Functions
"""
def getEdgeWithSmallestEdgeBetweennessRatio(g, listOfEdgesAlreadyConsidered, alreadyConsideredEBValues):
    "This function calculates edge betweenness ratio of all edges present in graph g"
    #print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*", listOfEdgesAlreadyConsidered)
    temp = g.edge_betweenness()
    edgeBetweennessList=[]

    for index, eb in enumerate(temp):
        edgeBetweennessList.insert(index,round(eb,3))

    temp = None
    #print(edgeBetweennessList)

    minEdgeBetweenness = max(edgeBetweennessList)
    for eb in edgeBetweennessList:
        if eb < minEdgeBetweenness and eb != 0.00 and eb not in alreadyConsideredEBValues:
            minEdgeBetweenness = eb

    #print("Min edge betweenness = %f"%minEdgeBetweenness)
    edgeList = []

    for index, edgeBetweenness in enumerate(edgeBetweennessList):
        e = g.es[index]
        #print(e.tuple, " ---------------- ",e.index," ------- %f"%edgeBetweenness)
        if(edgeBetweenness == minEdgeBetweenness and
           e.index not in listOfEdgesAlreadyConsidered and
           e.source != e.target):
            #print(e.tuple, " %%%%%%%%%%%%%%%%%%%%%%%%% ",e.index,"%%%%%%%%%%%% %f"%edgeBetweenness)
            #print(e.tuple, " *********************** %f" % round(edgeBetweenness,3))
            edgeList.append(e)
    if(len(edgeList) == 0 and len(alreadyConsideredEBValues) < 5):
        alreadyConsideredEBValues.append(minEdgeBetweenness)
        return getEdgeWithSmallestEdgeBetweennessRatio(g, listOfEdgesAlreadyConsidered, alreadyConsideredEBValues)
    else:
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

    source = edge.source
    target = edge.target

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
#inputGraph = Graph.Barabasi(n = 30 , m = 3, zero_appeal=3)
#inputGraph = Graph.Erdos_Renyi(n=25, p=0.08, directed=False, loops=False)
#inputGraph = Graph.Read_GraphML('karate.GraphML')
inputGraph = Graph.Read_Edgelist('0.edges',directed=False)

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
print("Modularity of Louvain algorithm = %f"%louvainCommunity.q)

girvanNewmanCommunity = inputGraph.community_edge_betweenness().as_clustering()
plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)
print("Modularity of Girvan-Newman algorithm = %f"%girvanNewmanCommunity.q)

isLocalMaximaAchievedCount = 20
maxModularity = -1
maxModularityCommunities = []
listOfEdgesAlreadyConsidered = []
idx = 1
index = 1
connectedComponents = getAllConnectedComponents(outputGraph, noOfVertices)
vertexCluster = getVertexClusteringFromConnectedComponents(outputGraph, connectedComponents)

while isLocalMaximaAchievedCount >= 0:
    temp = []
    edgeList = getEdgeWithSmallestEdgeBetweennessRatio(inputGraph, listOfEdgesAlreadyConsidered, temp)
    #print(len(edgeList))
    for edge in edgeList:
        #print(edge.tuple)
        tuples = getActualVertices(copyGraph, vertexCluster.membership, edge, listOfEdgesAlreadyConsidered)
        listOfEdgesAlreadyConsidered.append(edge.index)
        source = tuples[0]
        target = tuples[1]
        #print(outputGraph.vs.find(source),"+++++++++++",outputGraph.vs.find(target))
        outputGraph.add_edges([(source, target)])

    connectedComponents = getAllConnectedComponents(outputGraph, noOfVertices)
    vertexCluster = getVertexClusteringFromConnectedComponents(outputGraph, connectedComponents)
    componentList = outputGraph.clusters(mode="STRONG")

    inputGraph = copyGraph.copy()
    inputGraph.contract_vertices(vertexCluster.membership, combine_attrs=min(vertexCluster.membership))

    modularity = outputGraph.modularity(vertexCluster.membership)
    if(maxModularity < modularity):
        maxModularity = modularity
        index = idx
        isLocalMaximaAchievedCount = 20;
    else:
        isLocalMaximaAchievedCount -= 1

    print("%d   Modularity = %f" %(idx,modularity))
    #print("%d   Modularity with igraph  method = %f" % (idx, componentList.q))
    plot(vertexCluster, "outputGraph%d.png" %idx, mark_groups=True)
    idx += 1

print("Final index = %d"%index)
print("%d final  Modularity = %f" %(idx,modularity))