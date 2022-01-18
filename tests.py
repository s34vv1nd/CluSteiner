import subprocess
import os
from os import listdir
from os.path import isfile, join


if __name__ == '__main__':
  # subprocess.run(["pypy3", "./main.py", "Type_1_Large\\" + "10pr439.txt", str(0)]) 
  # exit(0)
  for seed in range(10):
    INPUT_FOLDER = "input_data\Type_1_Small"
    OUTPUT_FOLDER = "output_data\Type_1_Small"

    for file in listdir(INPUT_FOLDER):
      print(file, str(seed))
      subprocess.run(["pypy3", "./main.py", "Type_1_Small\\" + file, str(seed)])    

    INPUT_FOLDER = "input_data\Type_1_Large"
    OUTPUT_FOLDER = "output_data\Type_1_Large"

    for file in listdir(INPUT_FOLDER):
      print(file, str(seed))
      subprocess.run(["pypy3", "./main.py", "Type_1_Large\\" + file, str(seed)])    