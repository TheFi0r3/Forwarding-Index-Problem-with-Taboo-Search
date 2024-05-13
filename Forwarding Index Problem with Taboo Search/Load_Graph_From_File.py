
def load_graph_from_file(file_path):
    graph = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Extracting number of nodes and edges from comments
        num_nodes = int(lines[5]) #int(lines[1].split(': ')[1])
        num_edges = int(lines[6]) #int(lines[2].split(': ')[1])

        # Initialize empty adjacency matrix
        graph = [[0] * num_nodes for _ in range(num_nodes)]

        # Iterate through the lines starting from the 5th line
        for line in lines[7:]: # lines[4:]:
            node1, node2 = map(int, line.split())
            # Since it's an undirected graph, mark both edges
            graph[node1 - 1][node2 - 1] = 1
            graph[node2 - 1][node1 - 1] = 1

    return graph

# Example usage
file_path = 'file.txt'  # Replace 'graph.txt' with the path to your text file
loaded_graph = load_graph_from_file(file_path)
for row in loaded_graph:
    print(row)