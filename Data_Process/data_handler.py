import os
import sys

# print(sys.stdin.encoding)

dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 0 # TODO: (minsik.son) 이 값도 자동으로 넣도록 수정 필요함.
len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:len])
# print(dir_split)
# print(root_dir)
sys.path.append(root_dir)

# dictionary 형태의 json 파일 생성
# 첫 번째 라인은 key 로 사용

def get_유동자산_리스트(bPrint=False):
    # [1] open file
    file_path = root_dir + "\\data\\raw_data\\2020_1분기보고서_01_재무상태표_연결_20200613.txt"
    # file_path = root_dir + "\\data\\processed_data\\2020_1분기보고서_01_재무상태표_20200613.txt"
    
    file = open(file=file_path, mode='rt', encoding="utf-8")

    # [2] read first line
    __line = file.readline().split('\t')
    index_회사명 = 0
    index_항목명 = 0

    __row_size = 0
    for i in __line:
        # print(i)
        if i == "회사명":
            index_회사명 = __row_size
        if i == "항목명":
            index_항목명 = __row_size
        __row_size += 1

    # for DBG
    if bPrint == True:
        print("index_회사명: %s" % (index_회사명))
        print("index_항목명: %s" % (index_항목명))

    유동자산 = {}
    # [3] read data line
    for i in range(0, 500000):
        row_line = file.readline()
        if row_line == "":
            # print("EOF")
            break

        line = row_line.replace(" ", "").split('\t')
        if line[index_항목명] == "유동자산":
            # print(i, line[index_회사명], line[index_항목명], line[index_항목명 + 1])
            유동자산[line[index_회사명]] = line[index_항목명 + 1].replace(",", "")

    if bPrint == True:
        print(유동자산)
    return 유동자산


if __name__ == "__main__":
    get_유동자산_리스트()