## Optimization
As the result for the stochastic_page_rank estimation initially took about 90 seconds I have to find a way to optimize
the code to be faster.

### Optimizing stochastic_page_rank
Initially I was using random.randint to give me a random number and using that number in the node indexing to give me
a new target_node, but I realised soon that choosing a number and then finding a new target using that for 100 steps was
increasing my time by a lot. Then I realised that I could just use random.choice() and directly choose a target from the node.
Just by this I reduced my execution time by about 40 seconds.

```python
import random

nodes = list(graph.keys())
num = random.randint(0, len(nodes))
current_node = nodes[num]
