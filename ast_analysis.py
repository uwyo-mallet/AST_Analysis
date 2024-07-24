import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import json

def load_ast(ast_file_path):
    with open(ast_file_path, 'r') as file:
        ast = json.load(file)
    return ast

# Function to parse AST and build a graph
def parse_ast(ast_file):
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
    add_nodes_edges(ast_file)
    return G

# Function to extract graph characteristics
def analyze_graph(G):
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    degrees = dict(G.degree())
    transitivity = nx.transitivity(G)
    depth = nx.dag_longest_path_length(G) if nx.is_directed_acyclic_graph(G) else None
    
    print("Number of nodes:", num_nodes)
    print("Number of edges:", num_edges)
    print("Degrees of the nodes:", degrees)
    print("Transitivity:", transitivity)
    print("Depth of the tree:", depth)

# Function to visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", 
            font_size=8, font_weight="bold", arrows=True)
    plt.title("AST Graph")
    plt.show()

def main():
    ast_file = 'ast.txt'
    ast = load_ast(ast_file)
    G = parse_ast(ast)
    analyze_graph(G)
    visualize_graph(G)

if __name__ == "__main__":
    main()
