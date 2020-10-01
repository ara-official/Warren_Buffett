import requests
from ast import literal_eval # string to dictionray

import crtfc_key


API_HOST = "https://opendart.fss.or.kr/api/company.json"
CORP_CODE = "00126380"

def get_company_information(corp_code):
    URI = API_HOST + "?crtfc_key=" + crtfc_key.CRTFC_KEY + "&corp_code=" + corp_code
    res = requests.get(URI)

    return res

res = get_company_information(CORP_CODE)

print("[1] ", res.status_code)
print("[2] ", res.headers)
print("[3] ", res.text)
t = literal_eval(res.text)
print("[4] ", t["status"])
print("[4] ", t["stock_name"])