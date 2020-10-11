# [종목 조회 속도 개선] CREON 대신에, krx 와 opendart 를 통해 필요한 값 가져오도록 수정

# 그레이엄의 마지막 선물
from data_process import data_handler, file_inout

from restful.opendart import get_latest_financial_informantion
from restful.krx import get_latest_market_ohlcv

import datetime

DEBUG = False

def NCAV(weight=1, 유동자산_리스트=None, 부채총계_리스트=None): # TODO: BPS 고려
    print(NCAV.__name__)
    # [1] get raw date
    df_latest_market_ohlcv = get_latest_market_ohlcv() # all market
    # df_latest_market_ohlcv = get_latest_market_ohlcv(market="KOSPI")
    # df_latest_market_ohlcv = get_latest_market_ohlcv(market="KOSDAQ")
    # df_latest_market_ohlcv = get_latest_market_ohlcv(market="KONEX")

    # [2] get result
    loop = 0
    loop_count = 10
    print("[종목수]", len(df_latest_market_ohlcv.index))
    if DEBUG: exit() # for test

    # output
    date = datetime.datetime.today().strftime("%Y%m%d%H%M")
    output_file_name = date + "_NCAV.txt"
    path='./output/%s' % (output_file_name)
    file_inout.write_to_file(path=path, data="", option='w')

    for index in df_latest_market_ohlcv.index:
        # print(df_latest_market_ohlcv.loc[index])
        종목명 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[0]]
        시가 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[1]]
        종가 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[4]]
        시가총액 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[7]]

        # for test
        # if 종목명 != "아남전자":
        #     continue

        기업정보 = None
        유동자산 = None
        부채총계 = None
        if (유동자산_리스트 == None) and (부채총계_리스트 == None):
            기업정보 = get_latest_financial_informantion(corp_name=종목명) # <- 요 함수 개선 필요: data set 을 통으로 가져와서, 종목명으로 검색하도록 해야겠다..
            if 기업정보 == None:
                continue
            유동자산 = 기업정보[0]["thstrm_amount"].replace(",", "")
            부채총계 = 기업정보[5]["thstrm_amount"].replace(",", "")
        else:
            try:
                유동자산 = 유동자산_리스트[종목명]
            except KeyError:
                유동자산 = 0

            try:
                부채총계 = 부채총계_리스트[종목명]
            except KeyError:
                부채총계 = 0

        # exception case
        if (유동자산 == "-") or (유동자산 == ""):
            continue
        if (부채총계 == "-") or (부채총계 == ""):
            continue

        구매여부 = (int(유동자산) - int(부채총계)) > int(시가총액) * weight
        print(loop, "(", 구매여부, ")", 종목명, 종가, 유동자산, 부채총계, 시가총액)
        output = str(loop) + " (" + str(구매여부) + ") " + str(종목명) + "(종가:" + str(종가) + ") " + str(유동자산) + " - " + str(부채총계) + " > " + str(시가총액) + " * " + str(weight) + " ?"
        file_inout.write_to_file(path=path, data=output, option='a')

        # for test
        # if 종목명 == "아남전자":
        #     break

        # for test
        loop += 1
        if DEBUG:
            if loop > loop_count:
                break

if __name__ == "__main__":
    YEAR = "2020"
    MONTH = 9
    PRINT = False
    유동자산_리스트, 부채총계_리스트 = data_handler.get_유동자산_리스트(year=YEAR, month=MONTH, bPrint=PRINT)

    NCAV(유동자산_리스트=유동자산_리스트, 부채총계_리스트=부채총계_리스트)
