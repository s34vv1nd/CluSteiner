from os import fdopen
import os
import pathlib
import random
import sys
from SPGA import SPGA, build_clusteiner
from MST import MST
from SPH import SPH
from graph import ClusteredSteinerGraph
from timeit import default_timer as timer


def read_input(file_name: str):
  with open(file_name, "r") as f:
    name = f.readline().split(":")[1].strip()
    type = f.readline().split(":")[1].strip()
    dimensions = int(f.readline().split(":")[1].strip())
    n_clusters = int(f.readline().split(":")[1].strip())
    f.readline()
    edges = []
    for i in range(dimensions):
      edges.append([int(x) for x in f.readline().split()])
    f.readline()
    clusters = []
    for i in range(n_clusters):
      clusters.append([int(x) - 1 for x in f.readline().split()[1:] if x != "-1"])
  return (dimensions, n_clusters, edges, clusters)

if __name__ == '__main__':
  
  seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
  random.seed(seed)

  INPUT_FILE_NAME = sys.argv[1]
  (dimensions, n_clusters, edges, clusters) = read_input(INPUT_FILE_NAME)

  MIN_DIMENSIONS = int(sys.argv[5]) if len(sys.argv) > 5 else 0
  MAX_DIMENSIONS = int(sys.argv[4]) if len(sys.argv) > 4 else 5000
  if dimensions > MAX_DIMENSIONS or dimensions < MIN_DIMENSIONS:
    exit(0)

  nodes = [_ for _ in range(dimensions)]
  graph = ClusteredSteinerGraph(nodes, edges, clusters)

  alg = int(sys.argv[3]) if len(sys.argv) > 3 else 0

  start = timer()
  if alg == 0:
    result = SPGA(graph).run().best[1]
  elif alg == 1:
    result = min(build_clusteiner(graph, SPH) for _ in range(10000))
  elif alg == 2:
    result = MST(graph)[2]
  else:
    print("Invalid algorithm")
  end = timer()

  print("Best: " + str(result))
  print("Runtime: " + str(end - start) + " s")

  