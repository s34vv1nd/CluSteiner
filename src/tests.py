import pathlib
import subprocess
from os import listdir
from os.path import isfile, join
import sys


if __name__ == '__main__':
  alg = sys.argv[1] if len(sys.argv) > 1 else 0
  for instype in ['Type_6_Small', 'Type_5_Small', 'Type_1_Small']:
    print(instype)
    INPUT_FOLDER = "..\\input_data\\{}".format(instype)
    OUTPUT_FOLDER = "..\\output_data\\{}".format(instype)
    pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    for file in listdir(INPUT_FOLDER):
      for seed in range(30):
        print(file, str(seed))
        outfilename = OUTPUT_FOLDER + "\\" + file[:-4] + "_seed" + str(seed) + ".txt"
        with open(outfilename, "w") as f:
          subprocess.run(["pypy3", "./main.py", INPUT_FOLDER + "\\" + file, str(seed), str(alg)], stdout=f)