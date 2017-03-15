import igraph

edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (1,4), (2,3), (4,5), (4,6), (4,7), (5,6), (5,7), (6,7)]
graph = igraph.Graph(edges=edges, directed=False)

graph.vs["label"] = ["070","11","22","33","44","55","66","7"]

#graph = igraph.Graph

visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_color"] = "#d5acb9"
visual_style["vertex_size"] = 50

visual_style["bbox"] = (800,800)
visual_style["margin"] = 100

igraph.plot(graph,"before.png", **visual_style)


communities = [[],[]]

modularity = []
for i in range(0, graph.vcount()):
    for j in range(0, graph.neighbors(graph.vs.select(i)["id"])):
        print(i + "-------" + j)
        