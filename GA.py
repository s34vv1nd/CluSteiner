from cmath import inf
from collections import namedtuple
from math import factorial
import random
from SPH import SPH
from graph import ClusteredSteinerGraph, SteinerGraph

POP_SIZE = 100
MUTATION_RATE = 0.05
MAX_NO_IMPROVE = 500
MAX_GEN = 100
MAX_EVAL = 10000

GA_Result = namedtuple("GA_Result", ["gen_best", "best"])

class GA:
  def __init__(self, graph: ClusteredSteinerGraph):
    self.graph = graph
    self.n_genes = len(graph.clusters)
    self.current_gen = {}
    self.iter = 0
    self.total_eval = 0
    self.last_improve = 0
    self.gen_best = []

  def initialize(self):
    for i in range(POP_SIZE):
      permutation = random.sample(range(self.n_genes), self.n_genes)
      self.current_gen[tuple(permutation)] = inf

  def evaluate(self, pop, ind):
    if ((not (ind in pop)) or (pop[ind] == inf)) and (self.total_eval < MAX_EVAL):
      pop[ind] = build_clusteiner(self.graph, SPH, ind)
      self.total_eval += 1
    return pop[ind] if (ind in pop) else inf

  def evaluation(self):
    best = (None, inf)
    for ind in self.current_gen:
      val = self.evaluate(self.current_gen, ind)
      if val < best[1]:
        best = (ind, val)
    # print(self.iter, ": ", best)
    self.gen_best.append(best)
    return best

  def crossover(self, p1, p2):
    i, j = sorted(random.sample(range(self.n_genes), 2))
    c = list(p1)
    pos = [0 for _ in range(self.n_genes)]
    for k in range(j - i):
      pos[p1[i + k]] = i + k
    
    cnt = 0
    for k in range(self.n_genes):
      x = p2[(j + k) % self.n_genes]
      if pos[x] == 0:
        c[(j + cnt) % self.n_genes] = x
        cnt += 1
    return tuple(c)
  
  def mutate(self, p):
    i, j = sorted(random.sample(range(self.n_genes), 2))
    c = list(p)
    c[i], c[j] = c[j], c[i]
    return tuple(c)

  def selection(self, all):
    all = sorted(all.items(), key=lambda x: x[1])
    self.current_gen = dict(all[:POP_SIZE])

  def run(self):
    self.initialize()
    best = self.evaluation()
    for self.iter in range(MAX_GEN):
      offspring = {}
      for _ in range(POP_SIZE // 2):
        [p1, p2] = random.sample(self.current_gen.keys(), 2)
        c1 = self.crossover(p1, p2)
        c2 = self.crossover(p2, p1)
        offspring[c1] = self.evaluate(offspring, c1)
        offspring[c2] = self.evaluate(offspring, c2)
      
      for p in random.sample(self.current_gen.keys(), int(MUTATION_RATE * POP_SIZE)):
        c = self.mutate(p)
        offspring[c] = self.evaluate(offspring, c)

      self.selection({**self.current_gen, **offspring})
      gen_best = self.evaluation()
      if best[1] > gen_best[1]:
        best = gen_best
        self.last_improve = self.iter

      if self.total_eval >= MAX_EVAL or self.iter - self.last_improve >= MAX_NO_IMPROVE:
        break

    return GA_Result(self.gen_best, best)


def build_clusteiner(graph, solver, order=None):
  if not order:
    order = random_permutation(len(graph.clusters))
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
    tree = solver(stgraph)

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
  tree = solver(SteinerGraph(nodes, edges, targets))
  # print(sorted(tree.nodes))

  # add the inter-cluster links' cost
  sum += tree.cost()

  # return the total cost
  return sum

def random_permutation(n):
  p = [i for i in range(n)]
  for i in range(n):
    j = random.randint(0, i)
    p[i], p[j] = p[j], p[i]
  return p