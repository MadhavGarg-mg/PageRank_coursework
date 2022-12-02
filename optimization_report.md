## Optimization
Code optimization is any method of code modification to improve code quality and efficiency. In this
project, we optimize our code and make our code faster and more efficient. I have made use of 
dictionary comprehensions and random.choice() decrease the execution time of my code.

---
### Optimizing stochastic_page_rank
Initially, I was using random.randint() to give me a random number, so I could use that number in node 
indexing to give me a new target_node, but as I had to loop 100 million times, it took a lot of
time doing that. Instead, I choose to use random.choice() directly which lead to me cutting half 
my execution time by removing a redundant step getting repeated 100 million times. Using just this 
step I cut almost 45 seconds of execution time. Another way that I used to cut time was by using 
dictionary comprehensions for hit_counter which further cut some extra execution time. Just by using these
two methods, I was able to cut my time from 90 seconds to 43 seconds. The code also looks more
concise and clean after optimization.

```python
"""Initial code -> 90 seconds."""
import random

def stochastic_page_rank(graph, args):
    nodes = list(graph.keys())
    hit_counter = {}
    for i in nodes: 
        hit_counter[i] = 0 
    for repeat in range(args.repeats):  # This loop took 85 seconds
        num = random.randint(0, len(graph.keys()) - 1)
        current_node = nodes[num]
        for steps in range(args.steps):
            num = random.randint(0, len(graph[current_node]) - 1)
            current_node = graph[current_node][num]
        hit_counter[current_node] += 1 / args.repeats
    return hit_counter
```

```python
"""Optimized code -> 43 seconds."""
import random

def stochastic_page_rank(graph, args):
    nodes = list(graph.keys())
    hit_counter = {node: 0 for node in nodes}
    for repeats in range(args.repeats):  # This loop took 40 seconds
        current_node = random.choice(nodes) 
        for steps in range(args.steps):  
            current_node = random.choice(graph[current_node])
        hit_counter[current_node] += 1 / args.repeats
    return hit_counter
```
---

### Optimizing distribution_page_rank
The distribution_page_rank is a very fast function in comparison to the stochastic_page_rank 
function. It can give accurate results in under a second, but I could still optimize it to be a 
little faster. Initially, I was creating empty dictionaries for next_prob and node_prob 
and then putting key and values in the dictionary by going through a for loop, but instead of that
in the optimized version I am now using dictionary comprehension for them which decreases the 
execution time by about 1 millisecond. The code also looks more concise and clean after 
optimization. 

```python
"""Initial code -> 14 seconds."""

def distribution_page_rank(graph, args):
    nodes = list(graph.keys())
    next_prob = {}
    node_prob = {}
    for i in nodes:
        node_prob[i] = 1 / len(nodes) 
    for step in range(args.steps):
        for i in nodes:
            next_prob[i] = 0
        for node1 in nodes:
            p = node_prob[node1] / len(graph[node1])
            for target in graph[node1]:
                next_prob[target] += p
        for node in nodes:
            node_prob[node] = next_prob[node]
    return node_prob
```

```python
"""Optimized code -> 13 seconds."""

def distribution_page_rank(graph, args):
    node_prob = {node: 1 / len(list(graph.keys())) for node in list(graph.keys())}
    for step in range(args.steps):
        next_prob = {node: 0 for node in list(graph.keys())}
        for node1 in list(graph.keys()):
            p = node_prob[node1] / len(graph[node1])
            for target in graph[node1]:
                next_prob[target] += p
        for node in list(graph.keys()):
            node_prob[node] = next_prob[node]
    return node_prob
```
---
