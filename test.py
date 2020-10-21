# from restful.krx import test_lastest_market_fundamental

# test_lastest_market_fundamental()

from restful.opendart import get_latest_financial_informantion

dic = {}

# CORP_NAME = "벽산"
CORP_NAME = "삼성전자"

기업정보 = get_latest_financial_informantion(CORP_NAME, test=False)
print("result:", 기업정보)

# account_nm
for info_i in range(len(기업정보)):
    dic[기업정보[info_i]["account_nm"]] = 기업정보[info_i]["thstrm_amount"].replace(",", "") 
        
for key in dic.keys():
    print(key, ":", dic[key])

dic_2 = {}
dic_2["test"] = "hh"

dic.update(dic_2)

for key in dic.keys():
    print(key, ":", dic[key])

# 유동자산 = 기업정보[0]["thstrm_amount"].replace(",", "") 
# 비유동자산 = 기업정보[1]["thstrm_amount"].replace(",", "") 
# 자산총계 = 기업정보[2]["thstrm_amount"].replace(",", "") 
# 유동부채 = 기업정보[3]["thstrm_amount"].replace(",", "") 
# 비유동부채 = 기업정보[4]["thstrm_amount"].replace(",", "") 
# 부채총계 = 기업정보[5]["thstrm_amount"].replace(",", "")
# 자본금 = 기업정보[6]["thstrm_amount"].replace(",", "") 
# 이익잉여금 = 기업정보[7]["thstrm_amount"].replace(",", "") 
# 자본총계 = 기업정보[8]["thstrm_amount"].replace(",", "") 
# 매출액 = 기업정보[9]["thstrm_amount"].replace(",", "") 
# 영업이익 = 기업정보[10]["thstrm_amount"].replace(",", "") 
# 법인세차감전_순이익 = 기업정보[11]["thstrm_amount"].replace(",", "") 
# 당기순이익 = 기업정보[12]["thstrm_amount"].replace(",", "") 

# print("유동자산", 유동자산)
# print("비유동자산", 비유동자산)
# print("자산총계", 자산총계)
# print("유동부채", 유동부채)
# print("비유동부채", 비유동부채) 
# print("부채총계", 부채총계) 
# print("자본금", 자본금) 
# print("이익잉여금", 이익잉여금) 
# print("자본총계", 자본총계)
# print("매출액", 매출액) 
# print("영업이익", 영업이익) 
# print("법인세차감전_순이익", 법인세차감전_순이익) 
# print("당기순이익", 당기순이익) 