from cmath import inf
from typing import List
import random
from graph import ClusteredSteinerGraph, Graph, SteinerGraph, Tree
from heapq import *
from fibheap import *
from timeit import default_timer as timer


def cluster_SPH(graph: ClusteredSteinerGraph, order=None):
  if not order:
    order = random.sample(range(len(graph.clusters)), len(graph.clusters))
  # print("Clusters order:", order)

  n = max(graph.nodes) + 1

  # free vertices that do not belong to any cluster (yet)
  free = []
  for i in graph.nodes:
    if not i in graph.targets:
      free.append(i)

  # print(sorted(free))

  trees = []  # an array to store local trees
  sum = 0     # store the sum of costs of all local trees
  for c in order:
    # create a Steiner graph with current cluster's vertices and current remaining free vertices
    stgraph = SteinerGraph(graph.clusters[c] + free, graph.edges, graph.clusters[c])

    # run SPH for cluster c
    tree = SPH(stgraph)

    # store the local tree
    trees.append(tree)

    # eliminate used free vertices
    for i in free:
      if i in tree.nodes:
        free.remove(i)

    # add cost of local tree to sum
    sum += tree.cost()
  
  # create super nodes representing clusters
  nodes = free
  targets = []
  group = [i for i in range(n)]
  for tree in trees:
    nodes.append(n)
    targets.append(n)
    for i in tree.nodes:
      group[i] = n
    n += 1
  
  # create the edges between new nodes
  # st = timer()
  edges = [[inf for __ in range(n)] for _ in range(n)]
  m = len(graph.edges)
  for i in range(m):
    for j in range(m):
      edges[group[i]][group[j]] = min(edges[group[i]][group[j]], graph.edges[i][j])
  
  # en = timer()
  # print("Runtime (", m, " edges): ", en - st)

  # run SPH on the new compressed graph
  tree = SPH(SteinerGraph(nodes, edges, targets))
  # print(sorted(tree.nodes))

  # add the inter-cluster links' cost
  sum += tree.cost()

  # return the total cost
  return sum

def SPH(stgraph: SteinerGraph):
  # st = timer()
  n = max(stgraph.nodes) + 1
  is_target = [False for i in range(n)]
  for i in stgraph.targets:
    is_target[i] = True
  
  r = random.choice(stgraph.targets)
  tree = Tree([r], [])

  dist = []
  for i in range(n):
    if i == r:
      dist.append((0, None))
    else:
      dist.append((inf, None))

  heap = [(0, r)] 
  heapify(heap)
  cr = 0

  while len(heap) != 0:
    d_u, u = heappop(heap)

    if d_u > dist[u][0]:
      continue

    if is_target[u]:
      is_target[u] = False

      while dist[u][0] != 0:
        v = dist[u][1]
        tree.add_node(u)
        tree.add_edge(v, u, stgraph.edges[v][u])
        dist[u] = (0, v)
        heappush(heap, (0, u))
        u = v

      cr += 1
      if (cr == len(stgraph.targets)):
        break

    for (v, c) in stgraph.get_neighbors(u):
      if dist[v][0] > d_u + c:
        dist[v] = (d_u + c, u)
        heappush(heap, (d_u + c, v))

  # en = timer()
  # print("Runtime (", len(stgraph.nodes), " nodes): ", en - st)
  return tree