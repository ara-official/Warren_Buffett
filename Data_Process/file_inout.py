import os
import sys

# print(sys.stdin.encoding)

dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 0  # TODO: (minsik.son) 이 값도 자동으로 넣도록 수정 필요함.
len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:len])
# print(dir_split)
# print(root_dir)
sys.path.append(root_dir)

def write_to_file(path, data, option='w') :
    f = open(file=path, mode=option, encoding="utf-8")
    f.write("%s\n" % data)
    f.close()

def read_from_file(path) :
    output = []
    f = open(path, 'r')
    lines = f.readlines()
    for r in lines :
        output.append(r)

    return output
