import pathlib
import subprocess
import os
from os import listdir
from os.path import isfile, join
import sys


if __name__ == '__main__':
  alg = sys.argv[1] if len(sys.argv) > 1 else 0
  for instype in ['Type_1_Small', 'Type_1_Large', 'Type_6_Small', 'Type_6_Large', 'Type_5_Small', 'Type_5_Large', 'Type_2', 'Type_3_Large']:
    print(instype)
    INPUT_FOLDER = "input_data\{}".format(instype)
    OUTPUT_FOLDER = "output_data\Type_1_Small"
    pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    for file in listdir(INPUT_FOLDER):
      for seed in range(30):
        print(file, str(seed))
        subprocess.run(["pypy3", "./main.py", "{}\\".format(instype) + file, str(seed), str(alg)])    