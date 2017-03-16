import operator
from igraph import *
import igraph

"""
        Functions
"""        

def getClusterMembership (clusterList, noOfVertices):
    "This function converts cluster list into membership array"
    membership = []
    for i in range(noOfVertices):
        membership.insert(i, 0)
    print clusterList
    print clusterList.membership
    for cluster in clusterList:
        #print "*****",cluster
        if(len(cluster) == 1):
            vertex = cluster[0]
            #print "single vertex == %d" %vertex
            membership[vertex] = vertex
        else:
            minVertex = min(cluster)
            #print "minVertex ==== %d" %minVertex
            for c in cluster:
                #print c
                membership[c] = minVertex
    #print "-------",membership
    return membership

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

visual_style1 = {}
visual_style1["edge_curved"] = False
visual_style1["vertex_size"] = 18
visual_style1["vertex_label_size"] = 10
visual_style1["vertex_label_color"] = "#ffffff"
visual_style1["bbox"] = (700, 600)


"""
         Read a graph
"""
g = igraph.Graph.Erdos_Renyi(n=25, p=0.08, directed=False, loops=False)
#g = igraph.Graph.Read_GraphML('karate.GraphML')

g.vs["label"] = range(1000)
noOfVertices = g.vcount()

plot(g, "originalGraph.png", **visual_style)
print summary(g)

g1 = g.copy()
g2 = g.copy()
g1.delete_edges(g1.es())

"""
        Existing community detection algorithms: Louvain & Girvan-Newman
"""
louvainCommunity = g.community_multilevel()
plot(louvainCommunity, "louvain community.png", mark_groups=True)
#print louvainCommunity

"""
girvanNewmanCommunity = g.community_edge_betweenness().as_clustering()
plot(girvanNewmanCommunity, "girvan-newman community.png", mark_groups=True)
"""

"""
        Finding communities till all edges in original graph are not removed
"""
ebList = g.edge_betweenness()
ebList = sorted(ebList, key=float)
idx1 = 1
alreadyUsedTuples = []

while ebList:
    tupleId = 0
#  
#      Calculating edge betweenness and finding the smallest edge betweenness ratio
#
    for idx, eb in enumerate(ebList):
        print "%r ---> %f ---> %d" %(g.es[idx].tuple, eb, idx)
        if(g.es[idx].tuple[0]!= g.es[idx].tuple[1] and g.es[idx].tuple not in alreadyUsedTuples and g.are_connected(g.es[idx].tuple[0], g.es[idx].tuple[1])):
            alreadyUsedTuples.append(g.es[idx].tuple)            
            tupleId = idx  
            break
#
#        Adding the edge to graph G' and finding the connected components   
#      
    g.es[tupleId]['color'] ="green"
    plot(g, "G%d.png" %idx1, **visual_style)
       
    s = g.vs.find(g.es[tupleId].source)
    t = g.vs.find(g.es[tupleId].target)
    src = g1.vs.find(s['label'])
    trgt = g1.vs.find(t['label'])
    
    #print src
    #print trgt
    
    #src['color'] = "black"
    #trgt['color'] = "black"

    g1.add_edges([(src, trgt)])
    plot(g1, "G%d'.png" %idx1, mark_groups=True) 
    componentList = g1.clusters(mode=WEAK)
    print type(componentList.membership),"+++++", componentList.q

    membershipList = getClusterMembership(componentList, noOfVertices)
    vertexCluster = VertexClustering(g1, membership=membershipList)
    print type(vertexCluster.membership),"+++++", vertexCluster.q
    plot(vertexCluster, "cluster.png", mark_groups=True)
    print componentList.compare_to(vertexCluster)
#
#       Deleting the edge and re-organizing the original graph
#   
    g = g2.copy()
    g.contract_vertices(vertexCluster.membership, combine_attrs=min)
            
#
#       Re-calculating the edge betweenness ratio
#
    ebList = g.edge_betweenness()
    ebList = sorted(ebList, key=float)
    #print "************************** ebList size = %d" %len(ebList)
    #print ebList
#
#       Caclculating modularity
#
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>",componentList.q       

    idx1 += 1          
            
plot(g1, "output.png", **visual_style)