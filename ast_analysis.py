import subprocess
import json
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import csv

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
    depth = nx.dag_longest_path_length(G) if nx.is_directed_acyclic_graph(G) else None
    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "degrees": G.degree(),
        "transitivity": nx.transitivity(G),
        "depth": depth
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
    print("Max Depth:", max(result['depth'] for result in results))

def write_csv(results, output):
    with open(output, 'w', newline='') as csv_file:
        columns = ['file', 'num_nodes', 'num_edges', 'degrees', 'transitivity', 'depth']
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
        print(results)
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
