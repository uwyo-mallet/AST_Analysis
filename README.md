July 2024

University of Wyoming, College of Engineering
Lars Kotthoff
Grace Abawe

Python scripts for extracting graph characteristics from Abstract Syntax Trees

Ensure that the imported modules are installed and that the python virtual environment is activated.

To visualize AST graphs, specify the -g commandline flag before sourcefiles. If no -g is added, graphs will not be visualized.

For C code:
Then, to build the ASTs, extract characteristics, and visualize, run the following:

    python ast_analysis.py <sourcefiles.c>
    python ast_analysis.py -g <sourcefiles.c>

Multiple file paths can be specificied, it will prompt you for wether you would like to visualize graphs, and the output will be saved in 'c_results.csv'.

For python code:
To build the ASTs, extract characteristics, and visualize, run the following:

    python python_ast_analysis.py <sourcefiles.py> 
    python python_ast_analysis.py -g <sourcefiles.py> 

Multiple file paths can be specificied, it will prompt you for wether you would like to visualize graphs, and the output will be saved in 'p_results.csv'.



Example code files have been included in the ast_analysis folder, such as simple.c, matrix.c, and simple.py

Common issues:
If experiencing issues with uninstalled modules, try running:
    pip install networkx matplotlib
    sudo apt-get install graphviz

Tutorial for creating and activating a virtual environment:
    https://python.land/virtual-environments/virtualenv



Feature Extraction Documentation

Number of Nodes
Number of Edges
Degrees
    Min, Max, Mean, and Variance
    Number of edges that are incident to the vertex
Transitivity
    Probability for network to have adjacent nodes interconnected
    Calculated by dividing the total number of triangles by the number of triads (two edges with a shared vertex),
    then multiplying by 3
Leaf Depth
    Min, Max, and Mean
    Number of nodes on path from root to a leaf
Clustering Coefficients
    Min, Max, Mean, and Variance
    Measure of the degree to which nodes tend to cluster together
Entropy
    Degree, Depth
    Measure of disorder or number of ways system can be arranged
Betweenness Centrality
    Measure of centrality in a graph based on shortest paths. Measures the extent to which a node lies on the 
    paths between other nodes. A way of detecting the amount of influence a node has over the flow of information 
    in a graph.
    Calculated by summing the number of times a node is found on the shortest path between two nodes, 
    divided by the total number of shortest paths between the two nodes, for every pair of nodes in the graph.
Eigenvector Centrality
    Measure of the influence of a node in a connected network. A high eigenvector score means that a node is 
    connected to many nodes who themselves have high scores.
    Calculated using the adjacency matrix
Degree Assortativity
    Refers to the tendency of nodes to connect with other similar nodes over dissimilar nodes with respect to the 
    node degree. Assortativity is positive if nodes tend to connect to other nodes with similar degrees, and 
    negative if high-degree nodes tend to connect to low-degree nodes.
Average Eccentricity
    The average maximum distance between each vertex to all other vertices. 
Diameter
    Maximum Eccentricity. The maximum distance between all pairs of vertices.
Radius
    Minimum Eccentricity. The minimum among all the maximum distances between pairs of vertices.
Pagerank
    Computes a ranking of the nodes in the graph based on the structure of the incoming links. Similar to 
    eigenvector centrality.
    The eigenvector calculation is done by the power iteration method.
Edge Density
    Measures how densely the graph is connected
    Calculated by dividing number of edges by number of possible edges
Average Shortest Path Length
    The average of the shortest paths between all nodes
