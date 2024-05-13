import time
import random
import numpy as np

class Graph:
    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict
        self.nodes = sorted(list(self.graph_dict.keys()))

    def add_edge(self, node1, node2):
        if node1 not in self.graph_dict:
            self.graph_dict[node1] = []
        if node2 not in self.graph_dict:
            self.graph_dict[node2] = []
        self.graph_dict[node1].append(node2)
        self.graph_dict[node2].append(node1)  # Add reverse connection for undirected graph

    def get_neighbors(self, node):
        return self.graph_dict.get(node, [])

def tabu_search_all_pairs(graph, max_iterations, tabu_size):
    all_pairs_paths = {}
    nodes = list(graph.graph_dict.keys())

    for start_node in nodes:
        paths = {}
        for goal_node in nodes:
            if start_node == goal_node:
                paths[goal_node] = [start_node]
            else:
                path, _ = tabu_search(graph, start_node, goal_node, max_iterations, tabu_size)
                paths[goal_node] = path
        all_pairs_paths[start_node] = paths

    return all_pairs_paths

def tabu_search(graph, start, goal, max_iterations, tabu_size):
    current_solution = [start]
    current_node = start
    best_solution = current_solution[:]
    best_cost = float('inf')
    tabu_list = []

    for _ in range(max_iterations):
        neighbors = graph.get_neighbors(current_node)
        random.shuffle(neighbors)
        next_node = None
        min_cost = float('inf')

        for neighbor in neighbors:
            if neighbor not in current_solution and neighbor not in tabu_list:
                cost = len(current_solution) + 1
                if cost < min_cost or neighbor is goal:
                    min_cost = cost
                    next_node = neighbor

        if next_node is None:
            break

        current_solution.append(next_node)
        tabu_list.append(next_node)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        current_node = next_node
        if current_node == goal:
            current_cost = len(current_solution) - 1
            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost
                break

    return best_solution, best_cost

def print_graph_as_array(graph):

    nodes = sorted(list(graph.graph_dict.keys()))
    print("Shortest paths between all pairs of nodes:")
    print("   " + "   ".join(nodes))
    for start_node in nodes:
        row = start_node + " "
        for goal_node in nodes:
            path = all_pairs_paths[start_node][goal_node]
            row += "-".join(path) + " | "
        print(row)
        
    #nodes = graph.nodes
    num_nodes = len(nodes)
    adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if node2 in graph.graph_dict[node1] or node1 in graph.graph_dict[node2]:
                adjacency_matrix[i][j] = 1

    print("Graph as a 2D array (adjacency matrix):")
    print("   " + "   ".join(nodes))
    for i in range(num_nodes):
        row = nodes[i] + " "
        for j in range(num_nodes):
            row += str(adjacency_matrix[i][j]) + " "
        print(row)
        
def count_edges_crossed_by_paths(graph, all_pairs_paths):
    nodes = sorted(list(graph.graph_dict.keys()))
    num_nodes = len(nodes)
    edge_count_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for start_node in nodes:
        for goal_node in nodes:
            if start_node != goal_node:
                path = all_pairs_paths[start_node][goal_node]
                for i in range(len(path) - 1):
                    node1 = path[i]
                    node2 = path[i + 1]
                    edge_count_matrix[nodes.index(node1)][nodes.index(node2)] += 1
                    edge_count_matrix[nodes.index(node2)][nodes.index(node1)] += 1  # Add reverse edge count

    print("Graph as a 2D array (edge count matrix):")
    print("   " + "   ".join(nodes))
    for i in range(num_nodes):
        row = nodes[i] + " "
        for j in range(num_nodes):
            row += str(edge_count_matrix[i][j]) + " "
        print(row)
        
    edge_cross_count_list = get_edge_cross_count_list(edge_count_matrix)
    print("Number of times each edge is crossed:")
    print(edge_cross_count_list)

    max_edge_cross_count = calculate_max_edge_cross_count(edge_cross_count_list)
    print("Max edge cross count:", max_edge_cross_count)
        
def get_edge_cross_count_list(edge_count_matrix):
    edge_cross_count_list = []
    num_nodes = len(edge_count_matrix)
    
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):  # We only need to consider the upper triangle of the matrix
            edge_cross_count_list.append(edge_count_matrix[i][j])

    return edge_cross_count_list

def load_graph_from_file(file_path):
    graph = Graph()
    max_iterations = 100  # Default value
    tabu_size = 5  # Default value
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                # Read max_iterations and tabu_size from the first line
                first_line_values = lines[0].strip().split()
                if len(first_line_values) != 2:
                    raise ValueError("Error: Number of iterations and tabu size not set up in the file.")
                max_iterations, tabu_size = map(int, first_line_values)

                # Read graph data from subsequent lines
                for line_num, line in enumerate(lines[1:], start=2):
                    if line.strip():  # Check if the line is not empty
                        nodes = line.strip().split()  # Split the line into nodes
                        if len(nodes) >= 2:
                            node1 = nodes[0]
                            for node2 in nodes[1:]:
                                # Check if the edge already exists before adding it
                                if node2 not in graph.graph_dict.get(node1, []):
                                    graph.add_edge(node1, node2)
                        else:
                            raise ValueError(f"Error in line {line_num}: Each line should contain at least two nodes.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")
    except ValueError as e:
        raise ValueError(str(e))

    return graph, max_iterations, tabu_size

def calculate_max_edge_cross_count(edge_cross_count_list):
    if not edge_cross_count_list:
        return 0
    return max(edge_cross_count_list)

if __name__ == "__main__":
 
    file_path = "graph_data.txt"
    try:
        start_time = time.time()
        # Example usage:
        graph = Graph({
            'C': ['0','1','2','3','4','5'],
            '0': ['C','1','5'],
            '1': ['C','0','2'],
            '2': ['C','1','3'],
            '3': ['C','2','4'],
            '4': ['C','3','5'],
            '5': ['C','0','4']
        })
        
        graph, max_iterations, tabu_size = load_graph_from_file(file_path)
        print("Graph loaded from file:")
        print(graph.graph_dict)

        all_pairs_paths = tabu_search_all_pairs(graph, max_iterations, tabu_size)
        
        print_graph_as_array(graph)
        count_edges_crossed_by_paths(graph, all_pairs_paths)  

    except (FileNotFoundError, ValueError) as e:
        print(e)
        exit(1)  # Halt the program with exit code 1
    finally:
        end_time = time.time()  # Stop measuring execution time
        execution_time = end_time - start_time
        print("Execution time:", execution_time, "seconds")