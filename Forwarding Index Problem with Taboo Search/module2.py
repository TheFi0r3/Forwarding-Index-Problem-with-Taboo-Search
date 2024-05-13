import random
import numpy as np

class Graph:
    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def add_edge(self, node1, node2):
        if node1 not in self.graph_dict:
            self.graph_dict[node1] = []
        self.graph_dict[node1].append(node2)

    def get_neighbors(self, node):
        return self.graph_dict.get(node, [])

def tabu_search(graph, start, goal, max_iterations=100, tabu_size=5):
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
                cost = len(current_solution) + 1 + len(graph.get_neighbors(neighbor))
                if cost < min_cost:
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

    return best_solution, best_cost

if __name__ == "__main__":
    # Example usage:
    graph = Graph({
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': ['G'],
        'E': ['G'],
        'F': ['G'],
        'G': []
    })

    start_node = 'A'
    goal_node = 'G'

    solution, cost = tabu_search(graph, start_node, goal_node)
    print("Least amount of nodes to cross:", cost)
    print("Path:", solution)