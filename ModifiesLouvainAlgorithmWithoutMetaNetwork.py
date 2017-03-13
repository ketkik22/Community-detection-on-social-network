import operator
from igraph import *
import igraph


#
#       Visual style
#
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
#visual_style["layout"] = igraph.Graph.layout_random(dim=2)

#
#        Read a graph
#
g = igraph.Graph.Read_GraphML('karate.GraphML')
#g = igraph.Graph.Erdos_Renyi(n=25, p=0.08, directed=False, loops=False)
g.vs["label"] = range(1000)
plot(g, "originalGraph.png", **visual_style)
print summary(g)

g1 = g.copy()
g2 = g.copy()
g1.delete_edges(g1.es())

louvainCommunity = g.community_multilevel()
plot(louvainCommunity, "louvain community.png", **visual_style)
#print louvainCommunity

#girvanNewmanCommunity = g.community_edge_betweenness().as_clustering()
#plot(girvanNewmanCommunity, "girvan-newman community.png", **visual_style)

#
#       Finding communities till all edges in original graph are not removed
#
ebList = g.edge_betweenness()
ebList = sorted(ebList, key=float)

idx1 = 0
alreadyUsedTuples1 = []

while ebList:
    tupleId = 0
#   
#       Calculating edge betweenness and finding the smallest edge betweenness ratio
#    
    #for idx, eb in enumerate(ebList):
        #print "%r ---> %f ---> %d" %(g.es[idx].tuple, eb, idx)


    for idx, eb in enumerate(ebList):
        #print "%r ---> %f ---> %d" %(g.es[idx].tuple, eb, idx)
        if(g.es[idx].tuple not in alreadyUsedTuples1 and g.are_connected(g.es[idx].tuple[0], g.es[idx].tuple[1])):
            tupleId = idx
            alreadyUsedTuples1.append(g.es[tupleId].tuple)
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
    
    #src['color'] = "black"
    #trgt['color'] = "black"

    g1.add_edges([(src, trgt)])
   
#
#       Deleting the edge and re-organizing the original graph
#   
    g.delete_edges(g.es[tupleId])
    
#
#       Re-calculating the edge betweenness ratio
#
    ebList = g.edge_betweenness()
    ebList = sorted(ebList, key=float)
    #print "************************** ebList size = %d" %len(ebList)
    #print ebList
    
#
#       Caclculating modularity of detected communities
#
    comm = g1.clusters(mode=WEAK)
    
    modularityScore = g1.modularity(comm, weights=None)
    print comm
    print modularityScore, "---------------- at level ---------------", idx1
    
    plot(g1, "G%d'.png" %idx1, **visual_style1)    
    #print summary(g)
    idx1 += 1          
            
plot(g1, "output.png", **visual_style)
#print summary(g)




