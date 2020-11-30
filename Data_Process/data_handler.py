# TODO: folder 내의 파일 목록 활용해서 파일 가져오기 기능 구현

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

def calculate_quarter(month=0):
    quarter = 0
    if (1 <= month) & (month <= 3):
        quarter = 1
    elif (4 <= month) & (month <= 6):
        quarter = 2
    elif (7 <= month) & (month <= 9):
        quarter = 3
    elif (10 <= month) & (month <= 12):
        quarter = 4
    else:
        print("error!!")
        quarter = None
    return quarter

def get_prev_quarter(year, quarter):
    print("*** 이전 분기 자료가 기준입니다.", year, quarter)
    if quarter == 1:
        year -= 1
        quarter = 4
    else:
        quarter -= 1
    print("-->", year, quarter, "***")


    return int(year), int(quarter)

def get_유동자산_리스트(year=0, month=0, day=0, bPrint=False):
    if bPrint == True:
        print("year:", year)
    year = int(year)
    month = int(month)
    # NOTE: test 용으로 1분기 데이터만 이용.
    __분기 = calculate_quarter(month)

    # *** 이전 분기로 조정
    year, __분기 = get_prev_quarter(year, __분기)

    # [1] open file
    file_path = get_BS_file_path(year, __분기)
    print("file_path:", file_path)
    if file_path == None:
        print("잘못된 경로")
        exit()
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

# 현재는 수동으로 파일 추가하고 있음.
def get_BS_file_path(year=0, quarter=0):
    file_path = root_dir + "/data/raw_data/balance_sheet/"
    if year == 0:
        file_path = None # 중요한 지표이기 때문에, 정확한 입력이 필요합니다.
    elif year == 2020:
        if quarter == 1: file_path += "2020_1분기보고서_01_재무상태표_연결_20200613.txt"
        elif quarter == 2: file_path += "2020_반기보고서_01_재무상태표_연결_20201117.txt"
        elif quarter == 3: file_path += "2020_3분기보고서_01_재무상태표_연결_20201125.txt"
        else: file_path = None
    elif year == 2019:
        if quarter == 1: file_path += "2019_1분기보고서_01_재무상태표_연결_20201117.txt"
        elif quarter == 2: file_path += "2019_반기보고서_01_재무상태표_연결_20200423.txt"
        elif quarter == 3: file_path += "2019_3분기보고서_01_재무상태표_연결_20200617.txt"
        elif quarter == 4: file_path += "2019_사업보고서_01_재무상태표_연결_20200620.txt"
        else: file_path = None
    else:
        file_path = None

    print("file_path:", file_path)
    return file_path

def get_당기순이익_리스트(year=0, month=0, bPrint=False):
    if bPrint == True: print("year:", year)
    year = int(year)
    month = int(month)
    # NOTE: test 용으로 1분기 데이터만 이용.
    __분기 = calculate_quarter(month)

    # 이전 분기
    year, __분기 = get_prev_quarter(year, __분기)

    file_path = get_CE_file_path(year, __분기)

    if file_path == None: return None

    file = open(file=file_path, mode='rt', encoding="utf-8")

    # [2] read first line
    __line = file.readline().rstrip('\n').split('\t')

    print("line", __line)

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
        # line = row_line.replace(" ", "").split('\t') # 다행이 회사명 까지는 tab 으로 잘 구분되어 있음.
        line = row_line.split('\t') # 다행이 회사명 까지는 tab 으로 잘 구분되어 있음.
        # print(i, line)
        if (line[index_항목명] == "당기순이익") \
            or (line[index_항목명] == "당기순이익(손실)") \
            or (line[index_항목명] == "분기순이익") \
            or (line[index_항목명] == "분기순이익(손실)"): # 과거 포함 3년 정도 데이터 보여주기 때문에, 한 기업에 당기순이익 항목이 여러개 존재함.
            find = False
            for j in prev_line:
                if (year == 2020) and ((j == "2020.01.01") \
                    or (j == "2020.01.01(기초자본)")):
                    # print(i, line[index_회사명], line[index_항목명], line[index_항목명 + 1])
                    # print(line[index_회사명], index_회사명, line[index_항목명 + 1].replace(",", ""), index_항목명)
                    find = True
                    break 
                elif (year == 2019) and ((j == "2019.01.01") \
                    or (j == "2019.01.01(기초자본)")):
                    # print(i, line[index_회사명], line[index_항목명], line[index_항목명 + 1])
                    # print(line[index_회사명], index_회사명, line[index_항목명 + 1].replace(",", ""), index_항목명)
                    find = True
                    break

            if (find == True):
                당기순이익[line[index_회사명]] = line[index_항목명 + 1].replace(",", "")

        prev_line = line # 필요한 이유: 2020 년 자료 조회하면 2019 년 자료도 같이 나오는데, 걸러주기 위해 사용.

    # if bPrint == True:
    #     print(유동자산)
    return 당기순이익

    # for i in range(0, 500000):
    #     row_line = file.readline()
    #     if row_line == "":
    #         # print("EOF")
    #         break

    #     line = row_line.replace(" ", "").split('\t')
    #     if line[index_항목명] == "유동자산":
    #         # print(i, line[index_회사명], line[index_항목명], line[index_항목명 + 1])
    #         유동자산[line[index_회사명]] = line[index_항목명 + 1].replace(",", "")
    #     elif line[index_항목명] == "부채총계":
    #         부채총계[line[index_회사명]] = line[index_항목명 + 1].replace(",", "")

    # # if bPrint == True:
    # #     print(유동자산)
    # return 유동자산, 부채총계

def get_CE_file_path(year=0, quarter=0):
    file_path = root_dir + "/data/raw_data/changes_in_equity/"
    if year == 0:
        file_path = None
    elif year == 2020:
        if quarter == 1: file_path += "2020_1분기보고서_05_자본변동표_연결_20201118.txt"
        elif quarter == 2: file_path += "2020_반기보고서_05_자본변동표_연결_20201127.txt"
        elif quarter == 3: file_path += "2020_3분기보고서_05_자본변동표_연결_20201127.txt"
        else: file_path = None
    elif year == 2019:
        if quarter == 1: file_path += "2019_1분기보고서_05_자본변동표_연결_20201117.txt"
        elif quarter == 2:file_path = None
        elif quarter == 3:file_path += "2019_3분기보고서_05_자본변동표_연결_20201114.txt"
        elif quarter == 4:file_path += "2019_사업보고서_05_자본변동표_연결_20201127.txt"
        else: file_path = None
    else:
        file_path = None

    print("file_path:", file_path)
    return file_path

def get_영업이익(year=0, month=0, day=0, bPrint=False):
    if bPrint == True: print("year:", year)
    year = int(year)
    month = int(month)
    # NOTE: test 용으로 1분기 데이터만 이용.
    __분기 = calculate_quarter(month)

    # *** 이전 분기로 조정
    year, __분기 = get_prev_quarter(year, __분기)

    # [1] open file
    file_path = get_PL_file_path(year, __분기)
    if file_path == None:
        print("잘못된 경로")
        exit()
    file = open(file=file_path, mode='rt', encoding="utf-8")

    # [2] read first line
    __line = file.readline().rstrip('\n').split('\t')
    index_회사명 = 0
    index_항목명 = 0

    __row_size = 0
    for i in __line:
        if i == "회사명": index_회사명 = __row_size
        if i == "항목명": index_항목명 = __row_size
        __row_size += 1

    # for DBG
    if bPrint == True:
        print("index_회사명: %s" % (index_회사명))
        print("index_항목명: %s" % (index_항목명))

    영업이익 = {}
    # [3] read data line
    for i in range(0, 500000):
        row_line = file.readline()
        if row_line == "":
            # print("EOF")
            break

        line = row_line.replace(" ", "").split('\t')
        if (line[index_항목명] == "영업이익") \
            or line[index_항목명] == "영업이익(손실)":
            # print(i, line[index_회사명], line[index_항목명], line[index_항목명 + 1])
            영업이익[line[index_회사명]] = line[index_항목명 + 1].replace(",", "")

    return 영업이익

def get_PL_file_path(year=0, quarter=0):
    file_path = root_dir + "/data/raw_data/profit_and_loss/"
    if year == 0:
        file_path = None
    elif year == 2020:
        if quarter == 1: file_path += "2020_1분기보고서_03_포괄손익계산서_연결_20201118.txt"
        elif quarter == 2: file_path = None
        elif quarter == 3: file_path += "2020_3분기보고서_03_포괄손익계산서_연결_20201128.txt"
        else: file_path = None
    else:
        file_path = None

    return file_path

if __name__ == "__main__":
    # ret = get_유동자산_리스트(year=2020, month=11, bPrint=True)
    # ret = get_당기순이익_리스트(year=2020, month=11, bPrint=True)
    # ret = get_당기순이익_리스트(year=2019, month=11, bPrint=True)
    ret = get_영업이익(year=2020, month=11, bPrint=True)
    print(len(ret))
    print(ret)
    # print(ret["AJ네트웍스"])
    # print(ret["이트론"])
    # print(ret["이화산업"])
    # get_유동자산_리스트(year=2019, month=1, bPrint=True)
    # get_유동자산_리스트(year=2018, month=1, bPrint=True)
    # get_유동자산_리스트(year=2017, month=1, bPrint=True)
    # get_유동자산_리스트(year=2016, month=1, bPrint=True)
