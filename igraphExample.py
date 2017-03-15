import igraph

edges = [(0,8), (0,5), (0,1), (1,2), (2,3), (1,8), (1,6), (2,9), (3,7), (3,4), (3,5), (5,4), (5,9), (5,8), (4,1), (4,8), (6,2), (6,7), (6,9), (7,5), (7,8), (7,1), (8,3), (8,4), (9,7), (9,3)]
graph = igraph.Graph(edges=edges, directed=False)

graph.vs["label"] = ["0","1","2","3","4","5","6","7","8","9"]
#graph.es["weights"] = [4, 1, 8, 7, 6, 3, 5, 5, 8, 7, 6, 4, 4]

#graph = igraph.Graph

visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_color"] = "#AC0045"
visual_style["vertex_size"] = 50

visual_style["bbox"] = (800,800)
visual_style["margin"] = 100

igraph.plot(graph,"graph.png", **visual_style)
communities = graph.community_multilevel()

#comm = igraph.Graph.make_clusters(graph, membership=NULL, algorithm="community_multilevel" modularity=TRUE)
#print(communities)
igraph.plot(communities, "after.png")