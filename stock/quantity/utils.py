# refac item : 각 종목별로 조회 1번만 해서 필요한 data 다 글어오도록 수정 필요. 현재는 함수 별로 각자가 조회함;;

import os
import sys

dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 2 # TODO: (minsik.son) 이 값도 자동으로 넣도록 수정 필요함.
len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:len])
# print(dir_split)
# print(root_dir)
sys.path.append(root_dir)

from stock.creon.util import creon_0_Init
from stock.creon.util import creon
from stock.creon.util import creon_98_stocks_by_industry

from web_crawling import crawling_stock

from data_process import file_inout
from stock.creon.util import utils
from data_process import data_handler


class Quant_Utils:
    request_type_list = (
        creon.StockInfo.종목코드_0,
        creon.StockInfo.현재가_4,
        creon.StockInfo.총상장주식수_20,
        creon.StockInfo.부채비율_75,
        creon.StockInfo.당기순이익_88,
        creon.StockInfo.BPS_89,
        creon.StockInfo.분기당기순이익_104
    )

    def __init__(self, bPrint=False, use_crawler=False, skip_screen=False, bUseProxy=False):
        if use_crawler == True:
            self.crawling_stock_info = crawling_stock.Crawling_Stock_Info(skip_screen=skip_screen, bUseProxy=bUseProxy)
        self.유동자산_리스트 = data_handler.get_유동자산_리스트(bPrint)

        self.stock_info = creon.StockInfo()
        self.stock_name = None
        self.info_list = None

    def get_stock_info(self, stock_name):
        if self.stock_name == stock_name:
            return self.info_list

        info_list = self.stock_info.getInfo(stock_name, Quant_Utils.request_type_list)
        self.buffering_stock_info(stock_name, info_list)

        return info_list

    def buffering_stock_info(self, stock_name, info_list):
        self.stock_name = stock_name
        self.info_list = info_list

    def get_crawler(self):
        return self.crawling_stock_info

    def cal__CAGR(self): # Compund Annual Groth Rate
        pass
    def MDD(self): # Maximum Draw Down
        pass
    def cal__simple__intrinsic_value(self, stock_name): # 기업 내재 가치 계산
        print('get_intrinsic_value: %s' % (stock_name))
        # intrinsic_value = BPS + EPS * 10 ; (Book-value Per Stock) + (Earnings Per Stock * 10)
        pass
    def get_NCAV_by_date(self, date):
        pass

    def NCAV(self, stock_name, bCrawling=False, bPrint=False): # Net Current Asset Value. 순유동자산 = (유동자산 - 총부채) > (시가총액 * 1.5)
        info_list = self.get_stock_info(stock_name)
        
        유동자산 = self.get_CURRENT_ASSET(stock_name, bCrawling=bCrawling)
        if 유동자산 == '':
            유동자산 = 0
        유동자산 = float(유동자산)
        총부채 = self.get_TOTAL_DEBT(stock_name, bPrint=bPrint)
        시가총액 = self.get_MARKET_CAPITALIZATION(stock_name, bPrint=bPrint)
        bValuable = (유동자산 - 총부채) > (시가총액 * 1.5)
        print_1 = '(유동자산 - 총부채) > (시가총액 * 1.5)'
        print_2 = '= (%s - %s) > (%s * 1.5)' % (format(유동자산, ','), format(총부채, ','), format(시가총액, ','))
        print_3 = '= (%s) > (%s)' % (format(유동자산 - 총부채, ','), format(시가총액 * 1.5, ','))

        bBuy = (유동자산 - 총부채) > (시가총액 * 1.5)
        if 총부채 == 0:
            bBuy = False

        # 세후이익 계산 필요 (세후이익 > 0)
        당기순이익, 분기당기순이익 = self.get_NET_INCOME(stock_name)
        print_2 += '\n당기순이익: %s, 분기당기순이익: %s' % (format(당기순이익, ','), format(분기당기순이익, ','))
        if 당기순이익 < 0:
            bBuy = False
        if 분기당기순이익 < 0:
            bBuy = False

        if bBuy == True:
            print(print_1)
            print(print_2)
            print(print_3)
        
        return bBuy, print_2

    def get_CURRENT_ASSET(self, stock_name, bCrawling=False): # 유동자산 ?
        if bCrawling == True:
            stock_code = utils.Utils().get_code_from_name(stock_name)
            유동자산 = self.crawling_stock_info.get_CURRENT_ASSET(stock_name, stock_code[1:7])
            return 유동자산

        try:
            return self.유동자산_리스트[stock_name]
        except KeyError:
            return 0

    def get_TOTAL_DEBT(self, stock_name, bPrint=False): # 총 부채 = 부채율 * 총자산
        info_list = self.get_stock_info(stock_name)

        __상장주식수 = info_list[2]
        __부채비율 = info_list[3]
        __주당순자산 = info_list[5] # BPS (Book-value Per Share) == 주당순자산
        isBigListingStock = creon_98_stocks_by_industry.StocksByIndustry().isBigListingStock(stock_name)
        if isBigListingStock == True:
            __상장주식수 *= 1000
        __총자산 = __주당순자산 * __상장주식수
        # print('부채비율 : %s' % (부채비율))
        __총부채 = (__부채비율 / 100) * __총자산
        if __총부채 > 0:
            if bPrint == True:
                print('  총부채: %s' % (format(__총부채, ',')))
        return __총부채

    # [참고] https://money2.creontrade.com/e5/mboard/ptype_basic/plusPDS/DW_Basic_Read.aspx?boardseq=299&seq=84&page=1&searchString=&prd=&lang=&p=8833&v=8639&m=9505
    def get_MARKET_CAPITALIZATION(self, stock_name, bPrint=False): # 시가 총액 = 상장주식 수 * 현재가
        # 총자산 = 주당순자산(BPS) * 상장주식 수
        info_list = self.get_stock_info(stock_name)

        __현재가 = info_list[1]
        __상장주식수 = info_list[2]

        # 상장주식수 20억 이상이면 1000 단위로 제공됨
        isBigListingStock = creon_98_stocks_by_industry.StocksByIndustry().isBigListingStock(stock_name)
        if isBigListingStock == True:
            __상장주식수 *= 1000

        __시가총액 = __현재가 * __상장주식수
        if bPrint == True:
            print('시가총액: %s' % (format(__시가총액, ',')))
        return __시가총액

    def get_PBR(self, stock_name): # PBR = 현재가 / BPS
        info_list = self.get_stock_info(stock_name)

        __현재가 = info_list[1]
        __BPS = info_list[5]
        if float(__BPS) == 0:
            return 0
            
        __PBR = float(__현재가)/float(__BPS)
        return __PBR, float(__현재가), float(__BPS)

    def get_NET_INCOME(self, stock_name, bPrint=False):
        info_list = self.get_stock_info(stock_name)

        당기순이익 = info_list[4]
        분기당기순이익 = info_list[6]
        return 당기순이익, 분기당기순이익

# NOTE: (minsik.son) for test
if __name__ == "__main__":
    # creon_0_Init.Connection().do_creon_forced_reconnect()

    if creon_0_Init.Connection().is_creon_connected() == False:
        creon_0_Init.Connection().do_creon_forced_reconnect()
    else:
        print('[CREON] already connected~')
    util = Quant_Utils(skip_screen=True, bUseProxy=False)

    # NOTE: crawling 하기 전에 tor browser 를 실행하세요.
    # util.get_crawler().get_crwaler().move_to_url('https://check.torproject.org/')
    # util.get_crawler().get_crwaler().sleep(3)

    # util.get_crawler().loging_investing()
    # util.get_crawler().get_crwaler().sleep(3)

    # stock_list = (
    #     '삼성전자',
    #     'SK하이닉스',
    #     'CJ',
    #     '셀트리온',
    #     '금강공업',
    #     '아시아나항공',
    #     'NHN',
    #     '마니커'
    # )
    bListIsCode = True
    # stock_list = (
    #     # '메리츠화재',
    #     # '경방',
    #     '유수홀딩스',
    #     '동화약품',
    # 

    __marketType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피']
    stock_list = creon_98_stocks_by_industry.StocksByIndustry().getStockListByMarket(__marketType)
    __marketType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스닥']
    stock_list += creon_98_stocks_by_industry.StocksByIndustry().getStockListByMarket(__marketType)

    print(stock_list)

    path='./test.txt'
    count = 0
    stock_name = ''
    stock_code = ''
    sleep_count = 0
    for i in stock_list:
        count += 1
        # if count < 382: # <- 이 번호? 부터 crawling
        #     continue

        # sleep_count += 1

        # if sleep_count == 6:
        #     util.get_crawler().get_crwaler().sleep(30)
        #     sleep_count = 0

        if bListIsCode == True:
            stock_name = utils.Utils().get_name_from_code(i)
            stock_code = i
        else:
            stock_name = i
            stock_code = utils.Utils().get_code_from_name(i)

        print_1 = '[%s] 이름: %s, 코드: %s' % (count, stock_name, stock_code)

        구매여부, print_2 = util.NCAV(stock_name, bCrawling=False)
        # print_2 = '구매여부: %s' % (구매여부)

        print(print_1)
        print(print_2)
        print_5 = '=============================================================='
        print(print_5)

        if 구매여부 == False:
            continue
        
        PBR, 현재가, BPS = util.get_PBR(stock_name)
        print_4 = "PBR: %s, 현재가: %s, BPS: %s" % (PBR, 현재가, BPS)

        file_inout.write_to_file(path=path, data=print_1, option='a')
        file_inout.write_to_file(path=path, data=print_2, option='a')
        file_inout.write_to_file(path=path, data=print_4, option='a')
        file_inout.write_to_file(path=path, data=print_5, option='a')
