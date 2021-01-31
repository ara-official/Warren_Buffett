# NOTE: opendart 는 하루 10,000 회 조회 제한이 있습니다.
import datetime

import requests
from ast import literal_eval # parse, string to dictionray

# from crtfc_key import CRTFC_KEY
# from parse_xml import get_corp_code_by_corp_name
from restful.crtfc_key import CRTFC_KEY
from restful.parse_xml import get_corp_code_by_corp_name
API_HOST = "https://opendart.fss.or.kr/api/"

# 상장기업 재무정보

# DEBUG = True
DEBUG = False

def get_company_information(corp_name):
    corp_code = get_corp_code_by_corp_name(corp_name)
    if corp_code == None:
        if DEBUG: print("corp_code:", corp_code)
        return None

    URI = API_HOST + "company.json" + "?crtfc_key=" + CRTFC_KEY + "&corp_code=" + corp_code
    res = requests.get(URI)
 
    if res.status_code != 200:
        if DEBUG: print("[warn] corp_code 가 잘못되었습니다", corp_code)

    return res


# 1분기보고서, 반기보고서, 3분기보고서, 사업보고서
Q1 = "11013"
Q2 = "11012"
Q3 = "11014"
Q4 = "11011"
QUARTER = [
    Q1, Q2, Q3, Q4
]

def get_financial_information(corp_name, bsns_year=2020, reprt_code=None):
    if DEBUG: print(get_financial_information.__name__)

    corp_code = get_corp_code_by_corp_name(corp_name)
    if corp_code == None:
        if DEBUG: print("[warn] wrong corp_code:", corp_code)
        return None

    if reprt_code != None:
        URI = API_HOST + "fnlttSinglAcnt.json" + "?crtfc_key=" + CRTFC_KEY + "&corp_code=" + corp_code + "&bsns_year=" + str(bsns_year) + "&reprt_code=" + reprt_code
        if DEBUG: print("URI: ", URI)
        res = requests.get(URI)

        if res.status_code != 200:
            if DEBUG: print("[warn] corp_code 가 잘못되었습니다", corp_code, res.status_code)
            return None
        return res
    else:
        if DEBUG: print("[warn] wrong reprt_code", reprt_code)
        return None

def get_latest_financial_informantion(corp_name, test=False):
    year = datetime.datetime.today().strftime("%Y")

    if DEBUG: print("year: ", year)

    # for y in range(int(year), int(year) - 2, -1):
        # for j in range(len(QUARTER)-1, 0, -1):
    # if DEBUG: print("QUARTER[", j + 1, "]:", QUARTER[j])
    # 꼼수
    y = 2020
    j = 2
    reprt_code = QUARTER[j]
    res_2 = get_financial_information(corp_name=corp_name, bsns_year=str(y), reprt_code=reprt_code)
    if res_2 == None:
        print("get_latest_financial_informantion 1 :", corp_name)
        return None

    res_2_decode = res_2.content.decode("utf-8")
    t_2 = literal_eval(res_2_decode)

    if t_2["status"] == "000": # success
        if DEBUG: print(len(t_2["list"]))

        # 최근, 이전
        if test == True:
            for i in range(0, len(t_2["list"])):
                if (t_2["list"][i]["account_nm"] == "유동자산") & (i > 0):
                    break

                print(i, t_2["list"][i]["account_nm"], ": ", t_2["list"][i]["thstrm_amount"])
            # break

        else:
            return t_2["list"]
    else:
        # - 000 :정상
        # - 010 :등록되지 않은 키입니다.
        # - 011 :사용할 수 없는 키입니다. 오픈API에 등록되었으나, 일시적으로 사용 중지된 키를 통하여 검색하는 경우 발생합니다.
        # - 020 :요청 제한을 초과하였습니다. 일반적으로는 10,000건 이상의 요청에 대하여 이 에러 메시지가 발생되나, 요청 제한이 다르게 설정된 경우에는 이에 준하여 발생됩니다.
        # - 100 :필드의 부적절한 값입니다. 필드 설명에 없는 값을 사용한 경우에 발생하는 메시지입니다.
        # - 800 :원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.
        # - 900 :정의되지 않은 오류가 발생하였습니다.
        if t_2["status"] == "020":
            print("reprt_code 를 확인하세요 (status:", t_2["status"], ")")
            # exit()
        if DEBUG: print("reprt_code 를 확인하세요 (status:", t_2["status"], ")")

    return None


if __name__ == "__main__":
    # CORP_NAME = "삼성전자"
    CORP_NAME = "SK하이닉스"
    # CORP_NAME = "CJ"

    # result = get_latest_financial_informantion(CORP_NAME, test=True)
    result = get_latest_financial_informantion(CORP_NAME, test=True)
    print("result:", result)
    exit()

    res = get_company_information(CORP_NAME)
    if res == None:
        exit()
    # print("[1] ", res)
    # print("[1] ", res.status_code)
    # print("[2] ", res.headers)
    # print("[3] ", res.content.decode("utf-8"))
    # print("[3] ", res.content)
    # print("[3] ", res.text)
    # t = literal_eval(res.content)
    # print("[4] ", t["status"])
    # print("[4] ", t["stock_name"])

    print("======================================")
    # bsns_year 도 마찬가지로 올해 기준으로 마이너스 시켜서 구하자
    for j in range(len(QUARTER)-1, 0, -1):
        if DEBUG: print("QUARTER[", j + 1, "]: ", QUARTER[j])
        reprt_code = QUARTER[j]
        res_2 = get_financial_information(corp_name=CORP_NAME, bsns_year="2020", reprt_code=reprt_code)
        res_2_decode = res_2.content.decode("utf-8")
        # print("[1] ", res_2)
        # print("[2] ", res_2_decode)
        t_2 = literal_eval(res_2_decode)

        if t_2["status"] == "000": # success
            if DEBUG: print(len(t_2["list"]))

            # 최근, 이전
            for i in range(0, len(t_2["list"])):
                if (t_2["list"][i]["account_nm"] == "유동자산") & (i > 0):
                    break

                print(i, t_2["list"][i]["account_nm"], ": ", t_2["list"][i]["thstrm_amount"])
                
            break
        else:
            print("reprt_code 를 확인하세요")