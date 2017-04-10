import operator
from igraph import *

"""
        Functions
"""        

def getClusterMembership (clusterList, noOfVertices):
    "This function converts cluster list into membership array"
    print (clusterList)
    print (clusterList.membership)
    clusterList.membership.clear()
    print(clusterList.membership)
    #membership.clear()
    #print(membership)
    for i in range(noOfVertices):
        clusterList.membership.insert(i, 0)
    for cluster in clusterList:
        #print "*****",cluster
        if(len(cluster) == 1):
            vertex = cluster[0]
            #print "single vertex == %d" %vertex
            clusterList.membership[vertex] = vertex
        else:
            minVertex = min(cluster)
            #print "minVertex ==== %d" %minVertex
            for c in cluster:
                clusterList.membership[c] = minVertex
    #return membership



def getSourceAndTargetVertices(src, trgt, membership, graph):
    "This function returns correct source and destination vertex that should be connected in G'"
    if(graph.are_connected(src, trgt)):
        return
    #else:
        #for v in membership:




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
#inputGraph = igraph.Graph.Read_GraphML('karate.GraphML')

inputGraph.vs["label"] = range(1000)
noOfVertices = inputGraph.vcount()

plot(inputGraph, "originalGraph.png", **visual_style)

outputGraph = inputGraph.copy()
copyGraph = inputGraph.copy()
outputGraph.delete_edges(outputGraph.es())

"""
        Existing community detection algorithms: Louvain & Girvan-Newman
"""
louvainCommunity = inputGraph.community_multilevel()
plot(louvainCommunity, "louvain community.png", mark_groups=True)
#print louvainCommunity

#girvanNewmanCommunity = inputGraph.community_edge_betweenness().as_clustering()
#plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)


"""
        Finding communities till all edges in original graph are not removed
"""
ebList = inputGraph.edge_betweenness()
ebList = sorted(ebList, key=float)
idx1 = 1
alreadyUsedTuples = []

while ebList:
    tupleId = 0
#
#      Calculating edge betweenness and finding the smallest edge betweenness ratio
#
    for idx, eb in enumerate(ebList):
        #print ("%r ---> %f ---> %d" %(inputGraph.es[idx].tuple, eb, idx))
        src = inputGraph.vs.find(inputGraph.es[idx].source)
        trgt = inputGraph.vs.find(inputGraph.es[idx].target)
        if(src!= trgt and inputGraph.es[idx].index not in alreadyUsedTuples and inputGraph.are_connected(src, trgt)):
            alreadyUsedTuples.append(inputGraph.es[idx].index)
            tupleId = idx
            break
#
#        Adding the edge to graph G' and finding the connected components   
#      
    inputGraph.es[tupleId]['color'] ="green"
    plot(inputGraph, "G%d.png" %idx1, **visual_style)

    s = outputGraph.vs.find(src.index)
    t = outputGraph.vs.find(trgt.index)
    print (src.index, "-", src['label'], "------------>", s.index, "-", s['label'])
    print(trgt.index, "-", trgt['label'], "------------>", t.index, "-", t['label'])


    #getSourceAndTargetVertices(src, trgt, componentList.membership, copyGraph)

    outputGraph.add_edges([(s, t)])
    componentList = outputGraph.clusters(mode="WEAK")
    plot(componentList, "G%d'.png" %idx1, mark_groups=True)


    #getClusterMembership(componentList, noOfVertices)
    #temp = VertexClustering( outputGraph, membership=membership)
    print (componentList.membership)
#
#       Deleting the edge and re-organizing the original graph
#   
    inputGraph = copyGraph.copy()
    inputGraph.contract_vertices(componentList.membership, combine_attrs=min)

#
#       Re-calculating the edge betweenness ratio
#
    ebList = inputGraph.edge_betweenness()
    ebList = sorted(ebList, key=float)
    #print "************************** ebList size = %d" %len(ebList)
    #print ebList
#
#       Caclculating modularity
#
    print ("//////////////////////////////////////////", componentList.q)
    idx1 += 1          

plot(outputGraph, "output.png", mark_groups=True)