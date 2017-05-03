from distutils.command.install import install

from igraph import *

"""
        Functions
"""
def getEdgeWithSmallestEdgeBetweennessRatio(graph, edgeBetweennessList, alreadyConsideredEBValues):
    "This function calculates edge betweenness ratio of all edges present in graph g"
    #print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*", listOfEdgesAlreadyConsidered)

    minEdgeBetweenness = max(edgeBetweennessList)
    for eb in edgeBetweennessList:
        if eb < minEdgeBetweenness and eb != 0.00 and eb not in alreadyConsideredEBValues:
            minEdgeBetweenness = eb

    edgeList = []
    alreadyConsideredEBValues.append(minEdgeBetweenness)
    #print(alreadyConsideredEBValues)

    for index, edgeBetweenness in enumerate(edgeBetweennessList):
        e = graph.es[index]
        #print(e.tuple, " ---------------- ",e.index," ------- %f"%edgeBetweenness)
        if edgeBetweenness == minEdgeBetweenness:
            #print(e.tuple, " %%%%%%%%%%%%%%%%%%%%%%%%% ",e.index,"%%%%%%%%%%%% %f"%edgeBetweenness)
            #print(e.tuple, " *********************** %f" % round(edgeBetweenness,3))
            edgeList.append(e)

    return edgeList

def calculateEdgeBetweenness(graph):
    "This method calculates edge betweenness and format it into 3 digits after decimal point"
    temp = graph.edge_betweenness()
    edgeBetweennessList = []

    for index, eb in enumerate(temp):
        edgeBetweennessList.insert(index, round(eb, 3))
    return edgeBetweennessList

"""
        Visual styles
"""
visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_color"] = "#ff3563"
visual_style["vertex_size"] = 30
visual_style["vertex_label_size"] = 15
visual_style["vertex_label_color"] = "#ffffff"
visual_style["bbox"] = (1500, 1600)

"""
         Read a graph
"""
# inputGraph = Graph.Barabasi(n = 100 , m = 4, zero_appeal=3)
inputGraph = read('lesmis.gml')
#inputGraph = Graph.Read_GraphML('karate.GraphML')
# inputGraph = Graph.Read_Edgelist('0.edges',directed=False)
#print("%%%%%%%%%%%%%%%%",summary(inputGraph))

#inputGraph.vs()['label'] = range(50)
#for v in inputGraph.vs():
    #v['label'] = v.id

noOfVertices = inputGraph.vcount()

plot(inputGraph, "inputGraph.png", **visual_style)

outputGraph = inputGraph.copy()
outputGraph.delete_edges(outputGraph.es())

"""
        Existing community detection algorithms: Louvain & Girvan-Newman
"""
louvainCommunity = inputGraph.community_multilevel()
plot(louvainCommunity, "louvain community.png", mark_groups=True)
print("\n************************* LOUVAIN ALGORITHM *************************")
print(summary(louvainCommunity))
print("Modularity of Louvain algorithm = %f\t\t" % louvainCommunity.q, "\n\n")


girvanNewmanCommunity = inputGraph.community_edge_betweenness().as_clustering()
plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)
print("************************* GIRVAN-NEWMAN ALGORITHM ********************")
print(summary(girvanNewmanCommunity))
print("Modularity of Girvan-Newman algorithm = %f" % girvanNewmanCommunity.q, "\n\n")


isLocalMaximaAchievedCount = 30
maxModularity = -1
index = 0
maxModularityCommunities = []
idx = 1
alreadyConsideredEBValues = []

edgeBetweennessList = calculateEdgeBetweenness(inputGraph)

while isLocalMaximaAchievedCount >= 0:

    print("**************************************************** Iteration %d" % idx)
    edgeList = getEdgeWithSmallestEdgeBetweennessRatio(inputGraph, edgeBetweennessList, alreadyConsideredEBValues)
    for edge in edgeList:
        #print(edge.tuple)
        source = edge.source
        target = edge.target
        # print(outputGraph.vs.find(source),"+++++++++++",outputGraph.vs.find(target))
        outputGraph.add_edges([(source, target)])

    communities = outputGraph.clusters(mode="STRONG")

    modularity = communities.q
    if (maxModularity < modularity):
        maxModularity = modularity
        index = idx
        maxModularityCommunities = communities
        isLocalMaximaAchievedCount = 50;
    else:
        isLocalMaximaAchievedCount -= 1

    print(summary(communities))
    print("Modularity = %f\t\t" % (modularity))
    # print("%d   Modularity with igraph  method = %f\t\t" % (idx, componentList.q),summary(vertexCluster))
    plot(communities, "outputGraph%d.png" % idx, mark_groups=True)
    idx += 1

print("\n\nMax modularity index = %d"%index)
print("Number of communities  =  ", len(set(maxModularityCommunities.membership)))
print("Modularity = %f\t\t" % (maxModularity))
plot(maxModularityCommunities, "outputGraph.png", mark_groups=True)
exit()