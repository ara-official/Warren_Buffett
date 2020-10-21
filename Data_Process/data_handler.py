import os
import sys

# print(sys.stdin.encoding)

dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 0  # TODO: (minsik.son) 이 값도 자동으로 넣도록 수정 필요함.
__len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:__len])
# print(dir_split)
# print(root_dir)
sys.path.append(root_dir)

# dictionary 형태의 json 파일 생성
# 첫 번째 라인은 key 로 사용


def get_유동자산_리스트(year=0, month=0, day=0, bPrint=False):
    if bPrint == True:
        print("year:", year)
    year = int(year)
    month = int(month)
    # NOTE: test 용으로 1분기 데이터만 이용.
    __분기 = 0
    if (1 <= month) & (month <= 3):
        __분기 = 1
    elif (4 <= month) & (month <= 6):
        __분기 = 2
    elif (7 <= month) & (month <= 9):
        __분기 = 3
    elif (10 <= month) & (month <= 12):
        __분기 = 4
    # else:
    #     print("get_유동자산_리스트 error!!")
    #     return 0
    # [1] open file
    file_path = ""
    if year == 0:
        file_path = root_dir + "/data/raw_data/2020_1분기보고서_01_재무상태표_연결_20200808.txt"
    elif year == 2020:
        if __분기 == 2:
            file_path = root_dir + "/data/raw_data/2020_1분기보고서_01_재무상태표_연결_20200613.txt"
        elif __분기 == 3:
            file_path = root_dir + "/data/raw_data/2020_1분기보고서_01_재무상태표_연결_20200808.txt"
        elif __분기 == 4:
            file_path = root_dir + "/data/raw_data/2020_1분기보고서_01_재무상태표_연결_20201007.txt"
        else:
            file_path = root_dir + "/data/raw_data/2020_1분기보고서_01_재무상태표_연결_20201007.txt"
    elif year == 2019:
        file_path = root_dir + "/data/raw_data/2019_1분기보고서_01_재무상태표_연결_20200516.txt"
    elif year == 2018:
        file_path = root_dir + "/data/raw_data/2018_1분기보고서_01_재무상태표_연결_20200404.txt"
    elif year == 2017:
        file_path = root_dir + "/data/raw_data/2017_1분기보고서_01_재무상태표_연결_20191113.txt"
    elif year == 2016:
        file_path = root_dir + "/data/raw_data/2016_1분기보고서_01_재무상태표_연결_20190418.txt"
        
        # file_path = root_dir + "/data/processed_data/2020_1분기보고서_01_재무상태표_20200613.txt"

    print("file_path:", file_path)
    file = open(file=file_path, mode='rt', encoding="utf-8")

    # [2] read first line
    __line = file.readline().rstrip('\n').split('\t')
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
    부채총계 = {}
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
        elif line[index_항목명] == "부채총계":
            부채총계[line[index_회사명]] = line[index_항목명 + 1].replace(",", "")

    # if bPrint == True:
    #     print(유동자산)
    return 유동자산, 부채총계

def get_당기순이익_리스트(year=2020, month=6, bPrint=False):
    if bPrint == True:
        print("year:", year)
    year = int(year)
    month = int(month)
    # NOTE: test 용으로 1분기 데이터만 이용.
    __분기 = 0
    if (1 <= month) & (month <= 3):
        __분기 = 1
    elif (4 <= month) & (month <= 6):
        __분기 = 2
    elif (7 <= month) & (month <= 9):
        __분기 = 3
    elif (10 <= month) & (month <= 12):
        __분기 = 4

    file_path = ""
    if year == 2020:
        if __분기 == 2:
            file_path = root_dir + "/data/raw_data/2020_1분기보고서_05_자본변동표_연결_20201017.txt"
        else: # 2분기
            file_path = root_dir + "/data/raw_data/2020_1분기보고서_05_자본변동표_연결_20201017.txt"
    else:
        file_path = root_dir + "/data/raw_data/2020_1분기보고서_05_자본변동표_연결_20201017.txt"

    print("file_path:", file_path)
    file = open(file=file_path, mode='rt', encoding="utf-8")

    # [2] read first line
    __line = file.readline().rstrip('\n').split('\t')

    index_회사명 = 0
    index_항목명 = 0

    __row_size = 0
    for i in __line:
        print(__row_size, i)
        if i == "회사명":
            index_회사명 = __row_size
        if i == "항목명":
            index_항목명 = __row_size
        __row_size += 1

    # for DBG
    if bPrint == True:
        print("index_회사명: %s" % (index_회사명))
        print("index_항목명: %s" % (index_항목명))

    당기순이익 = {}
    prev_line = ""
    # [3] read data line
    for i in range(0, 500000): # NOTE: 500000?
        row_line = file.readline()
        if row_line == "":
            print("EOF: ", i)
            break

        # line = row_line.replace(" ", "").split('\t') # 데이터는 tab 으로 구분됨. 그러나 몇몇 데이터는 space 와 tab 혼재되어 있음.. 문제임
        line = row_line.replace(" ", "").split('\t') # 다행이 회사명 까지는 tab 으로 잘 구분되어 있음.
        line_2 = row_line.split(' ').split('\t') # 다행이 회사명 까지는 tab 으로 잘 구분되어 있음.
        # print(line)
        if (line[index_항목명] == "당기순이익") or (line[index_항목명] == "당기순이익(손실)"): # 과거 포함 3년 정도 데이터 보여주기 때문에, 한 기업에 당기순이익 항목이 여러개 존재함.
            find = False
            for j in prev_line:
                if (j == "2020.01.01"):
                    # print(i, line[index_회사명], line[index_항목명], line[index_항목명 + 1])
                    # print(line[index_회사명], index_회사명, line[index_항목명 + 1].replace(",", ""), index_항목명)
                    find = True
                    break
            if (find == True):
                당기순이익[line[index_회사명]] = line[index_항목명 + 1].replace(",", "")

        prev_line = line_2

    # if bPrint == True:
    #     print(유동자산)
    return 당기순이익


if __name__ == "__main__":
    # ret = get_유동자산_리스트(year=2020, month=1, bPrint=True)
    ret = get_당기순이익_리스트(year=2020, month=6, bPrint=True)
    print(ret["이트론"])
    print(ret["이화산업"])
    # get_유동자산_리스트(year=2019, month=1, bPrint=True)
    # get_유동자산_리스트(year=2018, month=1, bPrint=True)
    # get_유동자산_리스트(year=2017, month=1, bPrint=True)
    # get_유동자산_리스트(year=2016, month=1, bPrint=True)
