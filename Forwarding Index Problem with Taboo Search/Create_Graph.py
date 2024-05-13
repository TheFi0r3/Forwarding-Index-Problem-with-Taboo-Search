import networkx as nx

def generate_wheel_graph(num_nodes):
    return nx.wheel_graph(num_nodes)

def generate_hypercube_graph(dimension):
    return nx.hypercube_graph(dimension)

def generate_de_bruijn_graph(n, k):
    return nx.de_bruijn_graph(n, k)

def generate_star_graph(num_nodes):
    return nx.star_graph(num_nodes - 1)

def generate_cycle_graph(num_nodes):
    return nx.cycle_graph(num_nodes)

def print_graph(graph):
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        print(f"{node} {' '.join([str(n) for n in neighbors])}")

if __name__ == "__main__":
    print("Choose a graph to generate:")
    print("1. Wheel Graph")
    print("2. Hypercube Graph")
    print("3. De Bruijn Graph")
    print("4. Star Graph")
    print("5. Cycle Graph")
    
    choice = int(input("Enter your choice (1-5): "))
    
    if choice == 1:
        num_nodes = int(input("Enter the number of nodes in the wheel: "))
        graph = generate_wheel_graph(num_nodes)
    elif choice == 2:
        dimension = int(input("Enter the dimension of the hypercube: "))
        graph = generate_hypercube_graph(dimension)
    elif choice == 3:
        n = int(input("Enter the order of the graph: "))
        k = int(input("Enter the alphabet size: "))
        graph = generate_de_bruijn_graph(n, k)
    elif choice == 4:
        num_nodes = int(input("Enter the number of nodes in the star: "))
        graph = generate_star_graph(num_nodes)
    elif choice == 5:
        num_nodes = int(input("Enter the number of nodes in the cycle: "))
        graph = generate_cycle_graph(num_nodes)
    else:
        print("Invalid choice!")
        exit(1)
    
    print("Generated graph:")
    print_graph(graph)