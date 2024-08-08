import subprocess
import json
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
from scipy.stats import entropy
import numpy as np
import csv
import re

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

def write_csv(results, output):
    with open(output, 'w', newline='') as csv_file:
        columns = ['file', 'num_nodes', 'num_edges', 'degrees', 'max_degree', 'min_degree', 'mean_degree', 
                'degree_variance', 'transitivity', 'depths', 'max_depth', 'min_depth', 'mean_depth',
                'clustering_coefficients', 'max_clustering', 'min_clustering', 'mean_clustering', 'clustering_variance',
                'degree_entropy', 'depth_entropy', 'node_types', 'edge_transitions']
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def main(file_paths, output, bool):
    results = []
    for file_path in file_paths:
        generate_ast(file_path, "ast_output.txt")
        ast = load_ast("ast_output.txt")
        G = parse_ast(ast)
        stats = analyze_graph(G)
        if (bool.casefold() == 'yes'): #visualize graph
            visualize_graph(G)
        stats['file'] = file_path
        results.append(stats)
    write_csv(results, output)
    aggregate_stats(results)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        file_paths = sys.argv[1:] #take multiple files
        output = 'c_results.csv'
        boolean = input('Would you like to visualize the inputs as graphs? (yes/no)')
        main(file_paths, output, boolean)
    else:
        print("Error: Specify C file path(s) as second argument")    
