import ast
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

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
    pos = graphviz_layout(G, prog='dot')
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=500, node_color="lightblue", 
            font_size=8, font_weight="bold", arrows=True)
    plt.show()

def main(file_path):
    with open(file_path, 'r') as file:
        python_code = file.read()
    root = ast.parse(python_code)
    build = BuildAST()
    G = build.build_graph(root)
    analyze_graph(G)
    visualize_graph(G)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        main(file_path)
    else:
        print("Error: specify python file path as second argument")
