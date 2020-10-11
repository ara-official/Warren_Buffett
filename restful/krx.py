# [REF]
# https://wikidocs.net/47449
# [API]
# https://github.com/sharebook-kr/pykrx
# [Terms]
# OHLC: Open High Low Close: 시가, 최고가, 최저가, 종가

import requests

from restful.parse_xml import get_corp_code_by_corp_name

DEBUG = True

from pykrx import stock
import datetime

def test():
    # tickers: 시세
    tickers = stock.get_market_ticker_list(market="KOSPI")
    tickers += stock.get_market_ticker_list(market="KOSDAQ")
    tickers += stock.get_market_ticker_list(market="KONEX")

    return tickers

def get_latest_market_ohlcv(market=""):
    retry_count = 10
    today = datetime.datetime.today().strftime("%Y%m%d")

    for i in range(0, retry_count):
        latest_date = str(int(today) - i)
        if DEBUG: print(latest_date)
        result = stock.get_market_ohlcv_by_ticker(latest_date, market)
        if result.empty == False:
            return result
        
    

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

if __name__ == "__main__":
    corp_name = "삼성전자"
    # if (DEBUG): print(corp_name, get_corp_code_by_corp_name(corp_name))
    # res = 실시간_시세(corp_name)

    # if (DEBUG): print(res)
    # if (DEBUG): print("res.status_code:", res.status_code)
    # if (DEBUG): print("res.text:", res.text)
    # if (DEBUG): print("res.content:", res.content.decode("utf-8"))

    # tickers = test()
    # print("tickers", tickers)

    # for i in range(len(tickers)):
    #     ticker_name = stock.get_market_ticker_name(tickers[i])

    #     print(ticker_name, tickers[i])


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