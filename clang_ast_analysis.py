import subprocess
import json
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
from scipy.stats import entropy
import numpy as np
import re
import argparse

def generate_ast(c_file_path, ast_file_path):
    clang_command = f"clang -Xclang -ast-dump=json -fsyntax-only {c_file_path} > {ast_file_path}"
    subprocess.run(clang_command, shell=True, check=True)

def load_ast(ast_file_path):
    with open(ast_file_path, 'r') as file:
        ast = json.load(file)
    return ast

def parse_ast(ast):
    G = nx.DiGraph()
    def add_nodes_edges(node, parent=None):
        if isinstance(node, dict):
            node_id = node.get('id', None)
            if node_id:
                G.add_node(node_id, kind=node.get('kind'))
                if parent:
                    G.add_edge(parent, node_id)
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        add_nodes_edges(value, node_id)
        elif isinstance(node, list):
            for item in node:
                add_nodes_edges(item, parent)
    add_nodes_edges(ast)
    return G

def analyze_graph(G):
    depths = dict(nx.single_source_shortest_path_length(G, min(G.nodes())))
    degrees = sorted((d for n, d in G.degree()), reverse=True)
    leaf_depths = [depth for node, depth in depths.items() if G.out_degree(node) == 0] #depth from root to leaves
    clustering_coefficients = list(nx.clustering(G).values())
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

    node_types = set()
    edge_transitions = []

    for node in G.nodes(data=True):
        node_kind = node[1]['kind']
        node_types.add(node_kind)

        for successor in G.successors(node[0]):
            successor_kind = G.nodes[successor]['kind']
            edge_transitions.append(f"{node_kind} -> {successor_kind}")
    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "degrees": degrees,
        "max_degree": max(degrees),
        "min_degree": min(degrees),
        "mean_degree": np.mean(degrees),
        "degree_variance": np.var(degrees),
        "transitivity": nx.transitivity(G),
        "depths": leaf_depths,
        "max_depth": max(leaf_depths),
        "min_depth": min(leaf_depths),
        "mean_depth": np.mean(leaf_depths),
        "clustering_coefficients": clustering_coefficients,
        "max_clustering": max(clustering_coefficients),
        "min_clustering": min(clustering_coefficients),
        "mean_clustering": nx.average_clustering(G),
        "clustering_variance": np.var(clustering_coefficients),
        "degree_entropy": entropy(degrees),
        "depth_entropy": entropy(leaf_depths),
        #Additional features (not in paper)
        "betweenness_centrality": nx.betweenness_centrality(G),
        "eigenvector_centrality": nx.eigenvector_centrality(G, max_iter=500),
        "assortativity": nx.degree_assortativity_coefficient(G),
        "average_eccentricity": avg_eccentricity,
        "diameter": diameter,
        "radius": radius,
        "pagerank": nx.pagerank(G, max_iter=500),
        "edge_density": edge_density,
        "average_shortest_path": avg_shortest_path,
        "node_types": sorted(list(node_types)),
        "edge_transitions": edge_transitions
    }

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", 
            font_size=8, font_weight="bold", arrows=True)
    plt.title("AST Graph")
    plt.show()

def aggregate_stats(results):
    print("Aggregate Statistics:")
    print("Total Nodes:", sum(result['num_nodes'] for result in results))
    print("Total Edges:", sum(result['num_edges'] for result in results))
    print("Average Transitivity:", sum(result['transitivity'] for result in results) / len(results))
    print("Max Depth:", max(result['max_depth'] for result in results))
    print("Average Degree Mean:", np.mean([result['mean_degree'] for result in results]))
    print("Average Clustering Coefficient:", np.mean([result['mean_clustering'] for result in results]))
    print("Average Eccentricity:", np.mean([result['average_eccentricity'] for result in results]))
    print("Average Edge Density:", np.mean([result['edge_density'] for result in results]))

def print_results(stats, file):
    print("Statistics for file:", file)
    print("Number of nodes:", stats['num_nodes'])
    print("Number of Edges:", stats['num_edges'])
    print("Degrees:", stats['degrees'])
    print("Maximum Degree:", stats['max_degree'])
    print("Minimum Degree:", stats['min_degree'])
    print("Mean Degree:", stats['mean_degree'])
    print("Degree Variance:", stats['degree_variance'])
    print("Transitivity:", stats['transitivity'])
    print("Leaf Depths:", stats['depths'])
    print("Max Depth:", stats['max_depth'])
    print("Min Depth:", stats['min_depth'])
    print("Mean Depth:", stats['mean_depth'])
    print("Clustering Coefficients:", stats['clustering_coefficients'])
    print("Max Clustering:", stats['max_clustering'])
    print("Min Clustering:", stats['min_clustering'])
    print("Mean Clustering:", stats['mean_clustering'])
    print("Clustering Variance:", stats['clustering_variance'])
    print("Degree Entropy:", stats['degree_entropy'])
    print("Depth Entropy:", stats['depth_entropy'])
    print("Betweenness Centrality:", stats['betweenness_centrality'])
    print("Eigenvector Centrality:", stats['eigenvector_centrality'])
    print("Assortativity:", stats['assortativity'])
    print("Average Eccentricity:", stats['average_eccentricity'])
    print("Diameter:", stats['diameter'])
    print("Radius:", stats['radius'])
    print("Pagerank:", stats['pagerank'])
    print("Edge Density:", stats['edge_density'])
    print("Average Shortest Path:", stats['average_shortest_path'])
    print("Node Types:", stats['node_types'])
    print("Edge Type Transitions:", stats['edge_transitions'])
    print("")

def main(file_paths, visualize):
    results = []
    for file_path in file_paths:
        generate_ast(file_path, "ast_output.txt")
        ast = load_ast("ast_output.txt")
        G = parse_ast(ast)
        stats = analyze_graph(G)
        if (visualize==True): #visualize graph
            visualize_graph(G)
        results.append(stats)
        print_results(stats, file_path)
    aggregate_stats(results)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        file_paths = sys.argv[1:] #take multiple files
        parser = argparse.ArgumentParser(description="Analyze Clang ASTs and extract graph features.")
        #The -g flag should be specific before input C files to visualize graphs
        parser.add_argument("-g", "--graph", action="store_true", help="Visualize the graph after processing.")
        parser.add_argument("files", nargs='+', help="List of input Clang AST files to process.")
        args = parser.parse_args()
        main(file_paths=args.files, visualize=args.graph)
    else:
        print("Error: Specify C file path(s).")    
