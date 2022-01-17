import subprocess
import os
from os import listdir
from os.path import isfile, join


if __name__ == '__main__':
  # subprocess.run(["pypy3", "./main.py", "Type_1_Large\\" + "50pcb442.txt", str(0)]) 
  # exit(0)

  INPUT_FOLDER = "input_data\Type_1_Small"
  OUTPUT_FOLDER = "output_data\Type_1_Small"

  for file in listdir(INPUT_FOLDER):
    for seed in range(30):
      print(file, str(seed))
      subprocess.run(["pypy3", "./main.py", "Type_1_Small\\" + file, str(seed)])    

  INPUT_FOLDER = "input_data\Type_1_Large"
  OUTPUT_FOLDER = "output_data\Type_1_Large"

  for file in listdir(INPUT_FOLDER):
    for seed in range(30):
      print(file, str(seed))
      subprocess.run(["pypy3", "./main.py", "Type_1_Large\\" + file, str(seed)])    