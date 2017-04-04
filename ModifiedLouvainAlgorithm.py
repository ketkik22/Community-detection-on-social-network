from igraph import *
import queue as queue

"""
        Functions
"""
def getEdgeWithSmallestEdgeBetweennessRatio(g, listOfEdgesAlreadyConsidered):
    "This function calculates edge betweenness ratio of all edges present in graph g"
    edgeBetweennessList = g.edge_betweenness()

    while edgeBetweennessList:
        minEdgeBetweenness = min(edgeBetweennessList)
        edgeList = [g.es[index] for index, eb in enumerate(edgeBetweennessList) if minEdgeBetweenness == eb]
        for edge in edgeList:
            if(edge.index not in listOfEdgesAlreadyConsidered):
                source = edge.source
                target = edge.target
                if(source != target):
                    return edge
                else:
                    edgeBetweennessList.remove(minEdgeBetweenness)

def getConnectedComponentUsingBFS(g, vertex):
    "This function finds a connected component starting this vertex using Breadth-First search algorithm and returns it"
    VisitedVertices = []
    q = queue.Queue()

    q.put(vertex)
    VisitedVertices.append(vertex)

    while not queue.Empty():
        v = q.get()
        for v1 in g.neighbors(v):
            if v1 not in VisitedVertices:
                VisitedVertices.append(v1)
                q.put(v1)

    return VisitedVertices


def getAllConnectedComponents(g, vCount):
    "This function finds out all connected components of the given graph and returns VertexClustering object"
    Components = []
    VerticesTraversed = []
    VerticesNotTraversed = []

    for vertex in g.vs():
        VerticesNotTraversed.append(vertex)

    while len(VerticesTraversed) < g.vcount():
        v = VerticesNotTraversed.pop()
        s = getConnectedComponentUsingBFS(g, v)
        VerticesNotTraversed.append(v)

        for vertex in s:
            VerticesNotTraversed.remove(vertex)
            VerticesTraversed.append(vertex)
        Components.append(s)

    print(Components)
    return Components


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

while isLocalMaximaAchievedCount >= 0:
    edge = getEdgeWithSmallestEdgeBetweennessRatio(inputGraph, listOfEdgesAlreadyConsidered)
    listOfEdgesAlreadyConsidered.append(edge.index)

    print(edge.tuple)
    source = edge.source
    target = edge.target

    outputGraph.add_edges([(source, target)])

    connectedComponents = getAllConnectedComponents(outputGraph, noOfVertices)

    componentList = outputGraph.clusters(mode="WEAK")
    inputGraph = copyGraph.copy()
    inputGraph.contract_vertices(componentList.membership, combine_attrs=min)

    if(maxModularity < componentList.q):
        maxModularity = componentList.q
        isLocalMaximaAchievedCount = 3;
    else:
        isLocalMaximaAchievedCount -= 1

    plot(outputGraph, "outputGraph%f.png" %maxModularity, **visual_style)



