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
    #print(sorted(edgeBetweennessList))

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
    if(len(edgeList) == 0 and len(alreadyConsideredEBValues) < 10):
        alreadyConsideredEBValues.append(minEdgeBetweenness)
        return getEdgeWithSmallestEdgeBetweennessRatio(g, listOfEdgesAlreadyConsidered, alreadyConsideredEBValues)
    else:
        return edgeList

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
    # inputGraph = Graph.Erdos_Renyi(n=25, p=0.08, directed=False, loops=False)
    inputGraph = read('football.gml')
    # inputGraph = Graph.Read_Edgelist('0.edges',directed=False)
    print("%%%%%%%%%%%%%%%%",summary(inputGraph))

    for v in inputGraph.vs():
        v['label'] = v.index

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
    print("************************* LOUVAIN ALGORITHM *************************")
    print(summary(louvainCommunity))
    print("Modularity of Louvain algorithm = %f\t\t" % louvainCommunity.q, "\n\n")

    girvanNewmanCommunity = inputGraph.community_edge_betweenness().as_clustering()
    plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)
    print("************************* GIRVAN-NEWMAN ALGORITHM ********************")
    print(summary(girvanNewmanCommunity))
    print("Modularity of Girvan-Newman algorithm = %f" % girvanNewmanCommunity.q, "\n\n\n")

    isLocalMaximaAchievedCount = 30
    maxModularity = -1
    index = 0
    maxModularityCommunities = []

    while isLocalMaximaAchievedCount >= 0:

        print("**************************************************** Iteration %d" % idx)
        temp = []
        edgeList = getEdgeWithSmallestEdgeBetweennessRatio(inputGraph, listOfEdgesAlreadyConsidered, temp)
        for edge in edgeList:
            # print(edge.tuple)
            #tuples = getActualVertices(copyGraph, vertexCluster.membership, edge, listOfEdgesAlreadyConsidered)
            listOfEdgesAlreadyConsidered.append(edge.index)
            source = edge.source
            target = edge.target
            # print(outputGraph.vs.find(source),"+++++++++++",outputGraph.vs.find(target))
            outputGraph.add_edges([(source, target)])

        communities = outputGraph.clusters(mode="STRONG")

        modularity = communities.q
        if (maxModularity < modularity):
            maxModularity = modularity
            index = idx
            maxModularityCommunities = communities.membership
            isLocalMaximaAchievedCount = 30;
        else:
            isLocalMaximaAchievedCount -= 1

        print("Number of communities  =  ", len(set(vertexCluster.membership)))
        print("Modularity = %f\t\t" % (modularity))
        # print("%d   Modularity with igraph  method = %f\t\t" % (idx, componentList.q),summary(vertexCluster))
        plot(vertexCluster, "outputGraph%d.png" % idx, mark_groups=True)
        idx += 1