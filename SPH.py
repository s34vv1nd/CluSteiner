from cmath import inf
from typing import List
import random
from graph import ClusteredSteinerGraph, Graph, SteinerGraph, Tree
from heapq import *
from fibheap import *
from timeit import default_timer as timer


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