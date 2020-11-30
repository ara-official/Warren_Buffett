# [REF]
# https://wikidocs.net/47449
# [API]
# https://github.com/sharebook-kr/pykrx
# [Terms]
# OHLC: Open High Low Close: 시가, 최고가, 최저가, 종가

import requests

from restful.parse_xml import get_corp_code_by_corp_name

DEBUG = True
RETRY_COUNT = 100

from pykrx import stock
import datetime

def test():
    # tickers: 시세
    tickers = stock.get_market_ticker_list(market="KOSPI")
    tickers += stock.get_market_ticker_list(market="KOSDAQ")
    tickers += stock.get_market_ticker_list(market="KONEX")

    return tickers

def get_latest_market_ohlcv(today=None, market=""):
    
    if today == None:
        today = datetime.datetime.today().strftime("%Y%m%d")

    if DEBUG == True: print(get_latest_market_ohlcv.__name__, today)

    today_datetime = datetime.datetime.strptime(today, "%Y%m%d")
    for i in range(0, RETRY_COUNT):
        
        latest_date = (today_datetime - datetime.timedelta(i)).strftime("%Y%m%d")
        if DEBUG: print(latest_date)
        result = stock.get_market_ohlcv_by_ticker(latest_date, market)
        if result.empty == False:
            return result

    if DEBUG: print("fail")
    return None

def test_latest_market_ohlcv():
    df_latest_market_ohlcv = get_latest_market_ohlcv()

    print(df_latest_market_ohlcv.loc['000020'])
    print(df_latest_market_ohlcv.columns)
    print(df_latest_market_ohlcv.index)

    loop = 0
    loop_count = 10
    for index in df_latest_market_ohlcv.index:
        # print(df_latest_market_ohlcv.loc[index])
        종목명 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[0]]
        시가 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[1]]
        종가 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[4]]
        시가총액 = df_latest_market_ohlcv.loc[index][df_latest_market_ohlcv.columns[7]]
        print(종목명, 종가, 시가총액)

        loop += 1
        if loop > loop_count:
            break

def get_lastest_market_fundamental(today=None):
    if today == None:
        today = datetime.datetime.today().strftime("%Y%m%d")

    if DEBUG == True:
        print(get_lastest_market_fundamental.__name__, today)

    today_datetime = datetime.datetime.strptime(today, "%Y%m%d")

    for i in range(0, RETRY_COUNT):
        latest_date = (today_datetime - datetime.timedelta(i)).strftime("%Y%m%d")
        if DEBUG: print(latest_date)
        result = stock.get_market_fundamental_by_ticker(latest_date)
        if result.empty == False:
            return result

    if DEBUG: print("fail")
    return None

def test_lastest_market_fundamental():
    df_lastest_market_fundamental = get_lastest_market_fundamental()

    # print(df_lastest_market_fundamental)
    # print(df_lastest_market_fundamental.loc['000020'])
    # print(df_lastest_market_fundamental.columns)
    # print(df_lastest_market_fundamental.index)

    loop = 0
    loop_count = 10
    for index in df_lastest_market_fundamental.index:
        # print(df_latest_market_ohlcv.loc[index])
        종목명 = df_lastest_market_fundamental.loc[index][df_lastest_market_fundamental.columns[0]]
        DIV = df_lastest_market_fundamental.loc[index][df_lastest_market_fundamental.columns[1]]
        BPS = df_lastest_market_fundamental.loc[index][df_lastest_market_fundamental.columns[2]]
        PER = df_lastest_market_fundamental.loc[index][df_lastest_market_fundamental.columns[3]]
        EPS = df_lastest_market_fundamental.loc[index][df_lastest_market_fundamental.columns[4]]
        PBR = df_lastest_market_fundamental.loc[index][df_lastest_market_fundamental.columns[5]]
        print(종목명, DIV, BPS, PER, EPS, PBR)

    #     loop += 1
    #     if loop > loop_count:
    #         break

# 장 열렸을 때만 사용 가능,,
def 실시간_시세(corp_name):
    # corp_code = get_corp_code_by_corp_name(corp_name)
    corp_stock_code = "005930"
    # 실시간_시세
    URI = "http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code=" + corp_stock_code
    # 공시정보
    # URI = "http://asp1.krx.co.kr/servlet/krx.asp.DisList4MainServlet?code=" + corp_stock_code + "&gubun=" + kor_eng # (K:국문/E:영문)
    # 재무종합
    # URI = "http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu?code=" + corp_code
    # 재무종합2
    # URI = "http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu2?code=" + corp_code
    # 재무종합3
    # URI = "http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu3?code=" + corp_code
    # 텍스트
    # URI = "http://asp1.krx.co.kr/servlet/krx.asp.XMLText?code=" + corp_code
    if (DEBUG): print("URI:", URI)
    res = requests.get(URI)
    return res
