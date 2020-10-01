import requests
import crtfc_key

API_HOST = "https://opendart.fss.or.kr/api/company.json"
CORP_CODE = "00126380"

def get_company_information(corp_code):
    URI = API_HOST + "?crtfc_key=" + crtfc_key.CRTFC_KEY + "&corp_code=" + corp_code
    res = requests.get(URI)

    return res

res = get_company_information(CORP_CODE)

print(res.status_code)
print(res.headers)
print(res.text)