from random import choice
import sys
import os
import time
import argparse
from progress import Progress


def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    node_list = []
    target_list = []
    dictionary_nodes_target = {}
    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()
        node_list.append(node)  # This will put the current nodes in the node_list
        if node == node_list[0]:  # This condition will check if the current node is the first node in the node_list
            target_list.append(target)  # This will put all the targets for the current node in the target_list
            # This is making the value of the node in the dictionary to be its target_list
            dictionary_nodes_target[node_list[0]] = target_list
            # If the node_list has more than 1 node in it then we will delete the node at the 1st index
            if len(node_list) > 1:
                del node_list[1]
        else:
            # This will reset the target list if the node is not the same as the 0th index in the node_list
            target_list = [target]
            del node_list[0]
    return dictionary_nodes_target


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    num_edges = 0
    print('Number of nodes:', len(graph.keys()))  # Using graph.keys() we can get all the nodes from the datafile
    new_edges = graph.values()  # Putting lists of all the values of graph.values() in a list
    for edge in new_edges:  # Going through each list
        num_edges += len(edge)  # Adding the length of each list and putting it into num_edges
    print('Number of edges:', num_edges)


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    nodes = list(graph.keys())  # Putting all the nodes in a list
    hit_counter = {node: 0 for node in nodes}  # Initializing the hit_counter to be 0 for every node
    for repeats in range(args.repeats):
        current_node = choice(nodes)  # Choosing a random node for each repeat
        for steps in range(args.steps):
            current_node = choice(graph[current_node])  # Choosing a random target for each step from the node
        # Adding to the hit_counter for the current_node after all the steps
        hit_counter[current_node] += 1 / args.repeats
    return hit_counter


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    # Initializing the node_prob to be 1 / (number of nodes) for all nodes
    node_prob = {node: 1 / len(list(graph.keys())) for node in list(graph.keys())}
    for step in range(args.steps):
        # Initializing the next_prob to be 0 for all nodes
        next_prob = {node: 0 for node in list(graph.keys())}
        for node1 in list(graph.keys()):
            # Putting node_prob for all nodes and dividing with their out degree
            p = node_prob[node1] / len(graph[node1])
            for target in graph[node1]:
                next_prob[target] += p  # Adding the probability to the next_prob for all targets
        for node in list(graph.keys()):
            node_prob[node] = next_prob[node]  # Replacing the node_prob for each node as the nex_prob for that element
    return node_prob


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100 * v:.2f}\t{k}' for k, v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
