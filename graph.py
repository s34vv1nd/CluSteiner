from typing import List
from heapq import *


class Graph:
  def __init__(self, nodes: List[int], edges: List[List[int]]) -> None:
    self.nodes = nodes.copy()
    self.edges = edges.copy()

  def get_neighbors(self, u):
    return [(v, self.edges[u][v]) for v in self.nodes if v != u]

class SteinerGraph(Graph):
  def __init__(self, nodes: List[int], edges: List[List[int]], targets: List[int]) -> None:
    super(SteinerGraph, self).__init__(nodes, edges)
    self.targets = targets.copy()

class ClusteredSteinerGraph(SteinerGraph):
  def __init__(self, nodes: List[int], edges: List[List[int]], clusters: List[List[int]]) -> None:
    self.clusters = clusters.copy()
    super(ClusteredSteinerGraph, self).__init__(nodes, edges, [i for _ in clusters for i in _])
      


class Tree:
  def __init__(self, nodes: List[int], edges: List=[]) -> None:
    self.nodes = nodes.copy()
    self.edges = edges.copy()

  def add_node(self, u):
    self.nodes.append(u)

  def add_edge(self, u, v, w):
    self.edges.append((u, v, w))

  def cost(self):
    return sum(w for (u, v, w) in self.edges)
