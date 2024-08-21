# Uses Python Abstract Syntax Trees to extract graph characteristics

import ast
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import entropy
import csv
import os

#Parse Python AST and build a graph
class BuildAST(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_node = 0
        self.node_stack = []

    def generic_visit(self, node):
        node_id = self.current_node
        self.graph.add_node(node_id, label=type(node).__name__)
        
        if self.node_stack:
            parent_id = self.node_stack[-1]
            self.graph.add_edge(parent_id, node_id)
        
        self.node_stack.append(node_id)
        self.current_node += 1
        
        super().generic_visit(node)
        
        self.node_stack.pop()
    
    def build_graph(self, root):
        self.visit(root)
        return self.graph

# Function to extract graph characteristics
def analyze_graph(G):
    depths = dict(nx.single_source_shortest_path_length(G, 0))
    leaf_depths = [depth for node, depth in depths.items() if G.out_degree(node) == 0] #depth from root to leaves
    degrees = sorted((d for n, d in G.degree()), reverse=True)
    clustering_coefficients = list(nx.clustering(G).values())
    #~~~
    #Additional Features (not in paper)
    #Convert the directed graph to an undirected graph to avoid SCC problems
    undirected_G = G.to_undirected()
    if nx.is_connected(undirected_G): #check if undirected graph is connected
        diameter = nx.diameter(undirected_G)
        radius = nx.radius(undirected_G)
        avg_shortest_path = nx.average_shortest_path_length(undirected_G)
        avg_eccentricity = np.mean(list(nx.eccentricity(undirected_G).values()))
    else:
        #Calculate diameter of the largest strongly connected component
        largest_cc = max(nx.connected_components(undirected_G), key=len)
        subgraph = G.subgraph(largest_cc)
        diameter = nx.diameter(subgraph)
        radius = nx.radius(subgraph)
        avg_shortest_path = nx.average_shortest_path_length(subgraph)
        avg_eccentricity = np.mean(list(nx.eccentricity(subgraph).values()))
    edge_density = G.number_of_edges() / (G.number_of_nodes() * (G.number_of_nodes() - 1)) if G.number_of_nodes() > 1 else 0
    return {
        #Number of Nodes and Edges
        "Nodes": G.number_of_nodes(),
        "Edges":  G.number_of_edges(),
        #Degree Analysis
        "Degrees": degrees,
        "Max Degree": max(degrees),
        "Min Degree": min(degrees),
        "Mean Degree": np.mean(degrees),
        "Degree Variance": np.var(degrees),
        #Transitivity
        "Transitivity":  nx.transitivity(G),
        #Depth analysis
        "Depths": leaf_depths,
        "Max Depth": max(leaf_depths),
        "Min Depth": min(leaf_depths),
        "Mean Depth": np.mean(leaf_depths),
        #Clustering Coefficients
        "Clustering Coefficients": clustering_coefficients,
        "Max Clustering": max(clustering_coefficients),
        "Min Clustering": min(clustering_coefficients),
        "Mean Clustering": nx.average_clustering(G),
        "Clustering Variance": np.var(clustering_coefficients),
        #Entropy
        "Degree Entropy": entropy(degrees),
        "Depth Entropy": entropy(leaf_depths),
        #Additional features (not in paper)
        "Betweenness Centrality": nx.betweenness_centrality(G),
        "Eigenvector Centrality": nx.eigenvector_centrality_numpy(G, max_iter=500),
        "Assortativity": nx.degree_assortativity_coefficient(G),
        "Average Eccentricity": avg_eccentricity,
        "Diameter": diameter,
        "Radius": radius,
        "Pagerank": nx.pagerank(G, max_iter=500),
        "Edge Density": edge_density,
        "Average Shortest Path": avg_shortest_path,
    }

# Function to visualize the graph
def visualize_graph(G):
    pos = graphviz_layout(G, prog='dot')
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=500, node_color="lightblue", 
            font_size=8, font_weight="bold", arrows=True)
    plt.show()

#Function to create graph out of AST
def process_file(path, bool):
    with open(path, 'r') as file:
        python_code = file.read()
    root = ast.parse(python_code)
    build = BuildAST()
    G = build.build_graph(root)
    stats = analyze_graph(G)
    if (bool.casefold() == 'yes'): #visualize graph
        visualize_graph(G)
    return stats

#Function to print aggregate statistics
def aggregate_stats(results):
    print("Aggregate Statistics:")
    print("Total Nodes:", sum(result['Nodes'] for result in results))
    print("Total Edges:", sum(result['Edges'] for result in results))
    print("Average Transitivity:", sum(result['Transitivity'] for result in results) / len(results))
    print("Max Depth:", max(result['Max Depth'] for result in results))
    print("Average Degree Mean:", np.mean([result['Mean Degree'] for result in results]))
    print("Average Clustering Coefficient:", np.mean([result['Mean Clustering'] for result in results]))
    print("Average Eccentricity:", np.mean([result['Average Eccentricity'] for result in results]))
    print("Average Edge Density:", np.mean([result['Edge Density'] for result in results]))


#Function to output to .csv file
def write_csv(results, output):
    with open(output, 'w', newline='') as file:
        columns = ['File', 'Nodes', 'Edges', 'Degrees', 'Max Degree', 'Min Degree', 'Mean Degree', 'Degree Variance', 
                'Transitivity', 'Depths', 'Max Depth', 'Min Depth', 'Mean Depth', 'Clustering Coefficients', 'Max Clustering',
                'Min Clustering', 'Mean Clustering', 'Clustering Variance', 'Degree Entropy', 'Depth Entropy',  
                'Betweenness Centrality', 'Eigenvector Centrality', 'Assortativity', 'Average Eccentricity', 
                'Diameter', 'Radius', 'Pagerank', 'Edge Density', 'Average Shortest Path',]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for result in results:
            writer.writerow(result)


def main(file_paths, output, bool):
    results = []
    for file_path in file_paths:
        stats = process_file(file_path, bool)
        stats['File'] = file_path
        results.append(stats)
    write_csv(results, output)
    aggregate_stats(results)
        

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        file_paths = sys.argv[1:] #take multiple files
        output = 'p_results.csv'
        boolean = input('Would you like to visualize the inputs as graphs? (yes/no)')
        main(file_paths, output, boolean)
    else:
        print("Error: Specify python file path(s) as second argument")
