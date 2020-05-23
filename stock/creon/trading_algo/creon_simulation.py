
import sys
import os

# add root path
dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 3
len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:len])
# print(dir_split)
sys.path.append(root_dir)

# from data_process import json_utils
from data_process import json_utils

class Simulation:
    def __init__(self):
        print("test 1")

    def set_json(self):
        pass

    def run(self):
        print("test 2")

if __name__ == '__main__':
    sim = Simulation()
    sim.run()