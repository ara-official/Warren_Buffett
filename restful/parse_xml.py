# https://wikidocs.net/21140

from xml.etree.ElementTree import parse

tree = parse("restful/data/CORPCODE.xml")
root = tree.getroot()
corp_list = root.findall("list")

DEBUG = False

# print(corp_list[0].findtext("corp_name"))
# print(corp_list[0].findtext("corp_code"))
# print(len(corp_list))
def get_corp_code_by_corp_name(corp_name):
    for i in range(0, len(corp_list)):
        if corp_list[i].findtext("corp_name") == corp_name:
            return corp_list[i].findtext("corp_code")
    if DEBUG: print("[warn] corp_name 이 잘못 되었습니다.", corp_name)



if __name__ == "__main__":
    corp_name = "삼성전자"
    corp_code = get_corp_code_by_corp_name(corp_name)
    print(corp_name)
    print(corp_code)