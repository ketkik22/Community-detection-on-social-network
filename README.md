# Community-detection-on-social-network


Community in a large social network is a set of nodes grouped together such that the
nodes within communities are densely connected internally than that of nodes belonging
to different communities. These help us to find clusters of nodes which have common
properties and evaluate relationships between them. For example, in a social network
like Facebook people represent nodes, interactions among them represent edges
and the communities are groups of people who follow same football club or support a
same presidential nominee. Identifying such communities allows us to evaluate individual
objects, interaction between them and predict missing information, Therefore,
analyzing social network data in real-world networks and detecting communities have
become a very important problem in various areas.
The problem of community detection revolves around finding such implicit communities
in which the nodes that exhibit similar properties or behaviors are grouped together.
Currently, there are several methods and techniques that deal with finding community
structure. One of the technique is to find an edge which joins two groups. To find such
edges various centrality measures are used. Alternative approach is to find a hierarchical
structure in given network. Another approach is to categorized nodes into groups in
order to maximize/minimize some cost function. Some of the algorithms based on these
approaches are Girvan-Newman algorithm based on edge betweenness, Louvain algorithm, 
Label propagation algorithm, Fast-greedy approach etc. 
After studying and analyzing the existing community detection algorithms, in this project
I am proposing a new algorithm which is a combination of Divisive Hierarchical Clustering
and Agglomerative Hierarchical Clustering. This experiment is based on the concept
of iteratively merging nodes into community using the edge betweenness. It is observed
that edge betweenness of edges residing within same community is much lesser
than that of belonging to different. Using this approach I will conduct an experiment
to find underlying structure of social network. After achieving this, I am aiming to compare
and contrast the new proposed algorithm with the existing algorithms and to analyze
the effects of this algorithm on the random graphs and real-world networks.
