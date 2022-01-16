from os import fdopen
import random
import sys
from GA import GA
from SPH import SPH, cluster_SPH
from graph import ClusteredSteinerGraph, Graph
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
  seed = sys.argv[2] if len(sys.argv) > 1 else 0
  random.seed(seed)
  INPUT_FOLDER = "input_data\\"
  OUTPUT_FOLDER = "output_data\\"
  # FILE_NAME = sys.argv[1] if len(sys.argv) > 1 else "Type_1_Small\\5berlin52.txt"
  FILE_NAME = sys.argv[1] if len(sys.argv) > 1 else "Type_1_Large\\150nrw1379.txt"
  INPUT_FILE_NAME= INPUT_FOLDER + FILE_NAME
  OUTPUT_FILE_NAME= OUTPUT_FOLDER + FILE_NAME.split(".")[0] + "_seed" + seed + ".txt"
  (dimensions, n_clusters, edges, clusters) = read_input(INPUT_FILE_NAME)

  # print(dimensions)
  nodes = [_ for _ in range(dimensions)]
  # print(nodes)
  # print(n_clusters)
  # print(edges)
  # print(clusters)

  graph = ClusteredSteinerGraph(nodes, edges, clusters)

  start = timer()
  result = GA(graph).run()
  # result = cluster_SPH(graph)
  end = timer()

  with open(OUTPUT_FILE_NAME, "w+") as f:
    f.write("Generations:\n")
    for i, gen in enumerate(result.gen_best):
      f.write(str(i) + ": " + str(gen) + "\n")
    f.write("Best: " + str(result.best) + "\n")
    f.write("Runtime: " + str(end - start) + " s")