from igraph import *
import queue as queue

"""
        Functions
"""
def getEdgeWithSmallestEdgeBetweennessRatio(g, listOfEdgesAlreadyConsidered):
    "This function calculates edge betweenness ratio of all edges present in graph g"
    edgeBetweennessList = g.edge_betweenness()
    minEdgeBetweenness = edgeBetweennessList[0]
    edge = g.es[0]

    for index, edgeBetweenness in enumerate(edgeBetweennessList):
        e = g.es[index]
        if(edgeBetweenness < minEdgeBetweenness and
           e.index not in listOfEdgesAlreadyConsidered and
           e.source != e.target):
            minEdgeBetweenness = edgeBetweenness
            edge = e
    return edge


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

def getVertexClusteringFromConnectedComponents(connectedComponents):
    "This function takes connected compoenents and cretaes vertex clustering object"
    for component in connectedComponents:
        for c in component:
            print(type(c))

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
inputGraph = Graph.Erdos_Renyi(n=25, p=0.08, directed=False, loops=False)
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

isLocalMaximaAchievedCount = 3;
maxModularity = -1;
maxModularityCommunities = []
listOfEdgesAlreadyConsidered = []
idx = 1;

while isLocalMaximaAchievedCount >= 0:
    edge = getEdgeWithSmallestEdgeBetweennessRatio(inputGraph, listOfEdgesAlreadyConsidered)
    listOfEdgesAlreadyConsidered.append(edge.index)

    print(edge.tuple)
    source = edge.source
    target = edge.target

    outputGraph.add_edges([(source, target)])

    connectedComponents = getAllConnectedComponents(outputGraph, noOfVertices)
    vertexCluster = getVertexClusteringFromConnectedComponents(connectedComponents)

    componentList = outputGraph.clusters(mode="WEAK")
    inputGraph = copyGraph.copy()
    inputGraph.contract_vertices(componentList.membership, combine_attrs=min)

    if(maxModularity < componentList.q):
        maxModularity = componentList.q
        isLocalMaximaAchievedCount = 3;
    else:
        isLocalMaximaAchievedCount = 1

    plot(outputGraph, "outputGraph%d.png" %idx, **visual_style)
    idx += 1