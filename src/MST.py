from cmath import inf
from SPH import SPH
from graph import ClusteredSteinerGraph, Graph, SteinerGraph, Tree

def MST(graph: ClusteredSteinerGraph):
  trees = []
  for cluster in graph.clusters:
    trees.append(Tree(set(cluster), Kruskal(Graph(cluster, graph.edges), len(cluster) - 1)))

  inner_cost = sum(tree.cost() for tree in trees)
  
  n = max(graph.nodes) + 1

  # free vertices that do not belong to any cluster (yet)
  free = []
  for i in graph.nodes:
    if not i in graph.targets:
      free.append(i)

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
  edges = [[inf for __ in range(n)] for _ in range(n)]
  m = len(graph.edges)
  for i in range(m):
    for j in range(m):
      edges[group[i]][group[j]] = min(edges[group[i]][group[j]], graph.edges[i][j])

  # run SPH on the new compressed graph
  inter_cost = inf
  for r in targets:
    tree = SPH(SteinerGraph(nodes, edges, targets), r)
    inter_cost = min(inter_cost, tree.cost())
  # print(sorted(tree.nodes))

  # return the total cost
  return (inner_cost, inter_cost, inner_cost + inter_cost)

def Kruskal(graph: Graph, k: int):
  edges = []
  for i in graph.nodes:
    for (j, c) in graph.get_neighbors(i):
      edges.append((c, i, j))
  edges.sort()

  result = []
  p = [-1 for _ in range(max(graph.nodes) + 1)]
  i = 0
  while len(result) < k:
    (c, u, v) = edges[i]
    u = root(p, u)
    v = root(p, v)
    if u != v:
      unify(p, u, v)
      result.append((u, v, c))
    i += 1
  return result

def root(p, u):
  if p[u] < 0:
    return u
  p[u] = root(p, p[u])
  return p[u]

def unify(p, u, v):
  if p[u] < p[v]:
    p[v] = u
  elif p[v] < p[u]:
    p[u] = v
  else:
    p[v] = u
    p[u] -= 1