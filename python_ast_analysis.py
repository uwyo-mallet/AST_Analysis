# Uses Python Abstract Syntax Trees to extract graph characteristics

import ast
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
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
    depth = nx.dag_longest_path_length(G) if nx.is_directed_acyclic_graph(G) else None
    return {
        "Nodes": G.number_of_nodes(),
        "Edges":  G.number_of_edges(),
        "Degrees": dict(G.degree()),
        "Transitivity":  nx.transitivity(G),
        "Depth": depth 
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
    print("Max Depth:", max(result['Depth'] for result in results))

#Function to output to .csv file
def write_csv(results, output):
    with open(output, 'w', newline='') as file:
        columns = ['File', 'Nodes', 'Edges', 'Degrees', 'Transitivity', 'Depth']
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
        output = 'results.csv'
        boolean = input('Would you like to visualize the inputs as graphs? (yes/no)')
        main(file_paths, output, boolean)
    else:
        print("Error: Specify python file path(s) as second argument")
