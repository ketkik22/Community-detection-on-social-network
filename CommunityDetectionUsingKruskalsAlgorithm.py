import operator
from igraph import *
import igraph

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

from unionfind import unionfind



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
#g = igraph.Graph.Read_GraphML('karate.GraphML')
x = 25
g = igraph.Graph.Erdos_Renyi(n=x, p=0.08, directed=False, loops=False)
g.vs["label"] = range(1000)
plot(g, "originalGraph.png", **visual_style)
print summary(g)

mst = g.copy()
mst.delete_edges(mst.es())

k = x % 10

priotrityQ = Q.PriorityQueue(maxsize=x)
unionDS = unionfind(x)

for edge in g.es():
    priotrityQ.put(edge["weight"], edge)
    
while not priotrityQ.empty():
    edge = priotrityQ.get()
    if(unionDS.find(edge.source) != unionDS.find(edge.target)):
        unionDS.union(edge.source, edge.target)
        mst.add_edges([(edge.source, edge.target)])
        
plot(mst, "MST.png", **visual_style)
    


