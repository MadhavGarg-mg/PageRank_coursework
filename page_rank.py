import random
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
        node_list.append(node)
        if node == node_list[0]:
            target_list.append(target)
            dictionary_nodes_target[node_list[0]] = target_list
            if len(node_list) > 1:
                del node_list[1]
        else:
            target_list = [target]
            del node_list[0]
            dictionary_nodes_target[node_list[0]] = target_list
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
    nodes = list(graph.keys())
    hit_counter = {node: 0 for node in nodes}
    # hit_counter = {}
    # for i in nodes:
    #     hit_counter[i] = 0
    for repeates in range(args.repeats):
        # num = random.randint(0, len(graph.keys()) - 1)
        # current_node = graph[current_node][num]
        current_node = random.choice(nodes)
        for steps in range(args.steps):
            current_node = random.choice(graph[current_node])
        hit_counter[current_node] += 1/args.repeats
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
    nodes = list(graph.keys())
    next_prob = {}
    node_prob = {node: 1 / len(nodes) for node in nodes}
    for steps in range(args.steps):
        for i in nodes:
            next_prob[i] = 0
        for node1 in nodes:
            p = node_prob[node1] / len(graph[node1])
            for target in graph[node1]:
                next_prob[target] += p
        for node in nodes:
            node_prob[node] = next_prob[node]
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
    print(graph)
    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
