# [종목 조회 속도 개선] CREON 대신에, krx 와 opendart 를 통해 필요한 값 가져오도록 수정
# NOTE: 화면 보호 모드 될 때, opendart 접속 끊기는 현상 존재.

# 그레이엄의 마지막 선물
from data_process import data_handler, file_inout

from restful.opendart import get_latest_financial_informantion
from restful.krx import get_latest_market_ohlcv, get_lastest_market_fundamental

import datetime
import json

import time

DEBUG = False

# 함수이름은 NCAV 이지만, 실제 동작은 오늘 기준 해당 종목의 재무 데이터 뽑아오는 것이다.
def latest_NCAV(dump_json=True, weight=1, 유동자산_리스트=None, 부채총계_리스트=None, 당기순이익_리스트=None, 영업이익_리스트=None, today=None): # TODO: BPS 고려
    print(latest_NCAV.__name__)
    if today == None:
        today = datetime.datetime.today().strftime("%Y%m%d")

    print("[0] data: " + today)
    print("[1] get raw date - ohlcv")
    df_latest_market_ohlcv = get_latest_market_ohlcv(today) # all market
    # df_latest_market_ohlcv = get_latest_market_ohlcv(market="KOSPI")
    # df_latest_market_ohlcv = get_latest_market_ohlcv(market="KOSDAQ")
    # df_latest_market_ohlcv = get_latest_market_ohlcv(market="KONEX")

    print("[2] get raw date - DIV/BPS/PER/EPS/PBR")
    df_lastest_market_fundamental = get_lastest_market_fundamental(today)

    # [2] get result
    loop = 0
    loop_count = 10
    print("[종목수]", len(df_latest_market_ohlcv.index), "(df_latest_market_ohlcv)")
    print("[종목수]", len(df_lastest_market_fundamental.index), "(df_lastest_market_fundamental)")

    # print(df_latest_market_ohlcv)
    # print(df_lastest_market_fundamental)
    # if DEBUG: exit() # for test

    # output
    date = today + datetime.datetime.today().strftime("%H%M")
    output_file_name = date + "_NCAV.txt"
    path='./output/%s' % (output_file_name)
    file_inout.write_to_file(path=path, data="", option='w')

    json_dict = dict()
    json_dict["date"] = date
    json_dict["list"] = []
    for index in df_latest_market_ohlcv.index:
        if (유동자산_리스트 == None) or (부채총계_리스트 == None) or (당기순이익_리스트 == None) or (영업이익_리스트 == None): # NOTE: 현재는 이미 저장되어 있는 값 사용함.
            time.sleep(0.01)

        # print(df_latest_market_ohlcv.loc[index])
        종목명 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[0]]
        시가 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[1]]
        종가 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[4]]
        시가총액 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[7]]

        # for test
        # if 종목명 != "아남전자":
        #     continue

        기업정보 = None
        유동자산 = None # 0
        부채총계 = None # 5
        당기순이익 = None
        영업이익 = None

        # get_latest_financial_informantion 사용할 경우 유효
        # 비유동자산 = None # 1
        # 자산총계 = None # 2
        # 유동부채 = None # 3
        # 비유동부채 = None # 4
        # 자본금 = None # 6
        # 이익잉여금 = None # 7
        # 자본총계 = None # 8
        # 매출액 = None # 9
        # 영업이익 = None # 10
        # 법인세차감전_순이익 = None # 11
        # 당기순이익 = None # 12
        dic_info = {}
        if (유동자산_리스트 == None) or (부채총계_리스트 == None) or (당기순이익_리스트 == None) or (영업이익_리스트 == None): # NOTE: 현재는 이미 저장되어 있는 값 사용함.
            기업정보 = get_latest_financial_informantion(corp_name=종목명) # <- 요 함수 개선 필요: data set 을 통으로 가져와서, 종목명으로 검색하도록 해야겠다..
            if 기업정보 == None:
                continue
            for info_i in range(len(기업정보)):
                dic_info[기업정보[info_i]["account_nm"]] = str(기업정보[info_i]["thstrm_amount"].replace(",", ""))

            try:
                유동자산 = dic_info["유동자산"]
            except KeyError:
                유동자산 = 0
            try:
                부채총계 = dic_info["부채총계"]
            except KeyError:
                부채총계 = 0
        else:
            try:
                유동자산 = 유동자산_리스트[종목명]
            except KeyError:
                유동자산 = 0
            try:
                부채총계 = 부채총계_리스트[종목명]
            except KeyError:
                부채총계 = 0
            try:
                당기순이익 = 당기순이익_리스트[종목명]
            except KeyError:
                당기순이익 = 0

            try:
                영업이익 = 영업이익_리스트[종목명]
            except KeyError:
                영업이익 = 0

        # exception case
        if (유동자산 == "-") or (유동자산 == "") or (유동자산 == "\n"):
            continue
        if (부채총계 == "-") or (부채총계 == "") or (부채총계 == "\n"):
            continue
        if (당기순이익 == "-") or (당기순이익 == "") or (당기순이익 == "\n"):
            continue
        if (영업이익 == "-") or (영업이익 == "") or (영업이익 == "\n"):
            continue

        # TODO: 당기순이익 등의 정보 필요함. 자본변동표 활용
        dic_info["유동자산"] = 유동자산
        dic_info["부채총계"] = 부채총계
        dic_info["당기순이익"] = 당기순이익
        dic_info["영업이익"] = 영업이익



        DIV=None
        BPS=None
        PER=None
        EPS=None
        PBR=None
        for index_2 in df_lastest_market_fundamental.index:
            종목명_2 = df_lastest_market_fundamental.loc[index_2][df_lastest_market_fundamental.columns[0]]
            if 종목명 == 종목명_2:
                DIV = df_lastest_market_fundamental.loc[index_2][df_lastest_market_fundamental.columns[1]]
                BPS = df_lastest_market_fundamental.loc[index_2][df_lastest_market_fundamental.columns[2]]
                PER = df_lastest_market_fundamental.loc[index_2][df_lastest_market_fundamental.columns[3]]
                EPS = df_lastest_market_fundamental.loc[index_2][df_lastest_market_fundamental.columns[4]]
                PBR = df_lastest_market_fundamental.loc[index_2][df_lastest_market_fundamental.columns[5]]
                
                # 검색한 행 삭제
                df_lastest_market_fundamental = df_lastest_market_fundamental.drop(index_2)
                break

        구매여부 = (int(유동자산) - int(부채총계)) > int(시가총액) * weight
        print(loop, "(", 구매여부, ")", 종목명, 종가, 유동자산, 부채총계, 시가총액)
        output = str(loop) + " (" + str(구매여부) + ") " + str(종목명) + "(종가:" + str(종가) + ") " + str(유동자산) + " - " + str(부채총계) + " > " + str(시가총액) + " * " + str(weight) + " ?"
        output += "(DIV:" + str(DIV) + ", BPS: " + str(BPS) + ", PER: " + str(PER) + ", EPS: " + str(EPS) + ", PBR: " + str(PBR) + ")"
        file_inout.write_to_file(path=path, data=output, option='a')
        if dump_json == True:
            output_json = {
                "종목명": str(종목명),
                "종가": str(종가),
                "구매여부": str(구매여부),
                "시가총액": str(시가총액),
                "가중치": str(weight),
                "DIV": str(DIV),
                "BPS": str(BPS),
                "PER": str(PER),
                "EPS": str(EPS),
                "PBR": str(PBR)
                }
            output_json.update(dic_info) # 합치기
            json_dict["list"].append(output_json)

        # for test
        # if 종목명 == "아남전자":
        #     break

        # for test
        loop += 1
        if DEBUG:
            if loop > loop_count:
                break

    

    if dump_json == True:
        output_json_file_name = date + "_NCAV.json"
        path='./json/%s' % (output_json_file_name)
        # json = {"date":date, "list":json_list}
        file_inout.write_to_file(path=path, data=json.dumps(json_dict, ensure_ascii=False, indent="\t"), option='w')
    
        # add to list.txt
        file_inout.write_to_file(path="./json/list.txt", data=output_json_file_name, option='a')

if __name__ == "__main__":
    # today = datetime.datetime.today()
    today = datetime.datetime.strptime("20200106", "%Y%m%d")

    YEAR = today.strftime("%Y")
    MONTH = today.strftime("%m")
    DAY = today.strftime("%d")
    date = today.strftime("%Y%m%d")
    print(YEAR, MONTH, DAY)
    today = today - datetime.timedelta(3)

    for i in range(101):
        search_day = today + datetime.timedelta(i*7)
        YEAR = search_day.strftime("%Y")
        MONTH = search_day.strftime("%m")
        DAY = search_day.strftime("%d")
        YDM = search_day.strftime("%Y%m%d")
        print(search_day, YDM)

        # weekday = search_day.weekday()
        # if (weekday == 5) or (weekday == 6):
        #     continue

        PRINT = False
        유동자산_리스트, 부채총계_리스트 = data_handler.get_유동자산_리스트(year=YEAR, month=MONTH, bPrint=PRINT)
        당기순이익_리스트 = data_handler.get_당기순이익_리스트(year=YEAR, month=MONTH)
        영업이익_리스트 = data_handler.get_영업이익(year=YEAR, month=MONTH)

        skip = (유동자산_리스트 == None) | (부채총계_리스트 == None) | (당기순이익_리스트 == None) | (영업이익_리스트 == None)
        if skip == True:
            continue

        latest_NCAV(dump_json=True, 유동자산_리스트=유동자산_리스트, 부채총계_리스트=부채총계_리스트, 당기순이익_리스트=당기순이익_리스트, 영업이익_리스트=영업이익_리스트, today=YDM)


    # latest_NCAV(dump_json=True, 유동자산_리스트=None, 부채총계_리스트=None, 당기순이익_리스트=None, 영업이익_리스트=None)
    # latest_NCAV(dump_json=True, 유동자산_리스트=유동자산_리스트, 부채총계_리스트=부채총계_리스트, 당기순이익_리스트=당기순이익_리스트, 영업이익_리스트=영업이익_리스트, today="20201130")
