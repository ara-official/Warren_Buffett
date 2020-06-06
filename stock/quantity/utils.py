import os
import sys

dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 2 # TODO: (minsik.son) 이 값도 자동으로 넣도록 수정 필요함.
len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:len])
print(dir_split)
print(root_dir)
sys.path.append(root_dir)

from stock.creon.util import creon_0_Init
from stock.creon.util import creon
from stock.creon.util import creon_98_stocks_by_industry

class Quant_Utils:
    def __init__(self):
        pass
    def cal__CAGR(self): # Compund Annual Groth Rate
        pass
    def MDD(self): # Maximum Draw Down
        pass
    def cal__simple__intrinsic_value(self, stock_name): # 기업 내재 가치 계산
        print('get_intrinsic_value: %s' % (stock_name))
        # intrinsic_value = BPS + EPS * 10 ; (Book-value Per Stock) + (Earnings Per Stock * 10)
        pass
    def NCAV(self, stock_name): 
        # Net Current Asset Value. 순유동자산
        # (유동자산 - 총부채) > (시가총액 * 1.5)
        유동자산 = self.get_CURRENT_ASSET(stock_name)
        총부채 = self.get_TOTAL_DEBT(stock_name)
        시가총액 = self.get_MARKET_CAPITALIZATION(stock_name)
        print('(유동자산 - 총부채) > (시가총액 * 1.5)')
        print('= (%s - %s) > (%s * 1.5)' % (유동자산, 총부채, 시가총액))
        print('= (%s) > (%s)' % (format(유동자산 - 총부채, ','), format(시가총액 * 1.5, ',')))
        bBuy = (유동자산 - 총부채) > (시가총액 * 1.5)
        
        # 세후이익 계산도 필요
        # 세후이익 > 0
        
        return bBuy

    def get_CURRENT_ASSET(self, stock_name): # 유동자산 ?
        유동자산 = 0
        stStockInfo = creon.StockInfo()
        # investing.com 기준 유동자산
        if stock_name == '삼성전자':
            유동자산 = 186739748
        elif stock_name == 'SK하이닉스':
            유동자산 =  15799759
        elif stock_name == 'CJ':
            유동자산 =  11471234.11
        elif stock_name == '셀트리온':
            유동자산 = 1977808.33
        elif stock_name == '금강공업':
            유동자산 = 371512.97 
        elif stock_name == '아시아나항공':
            유동자산 = 1508466.67
        elif stock_name == 'NHN':
            유동자산 = 999564.49
        elif stock_name == '마니커':
            유동자산 = 31745.07
        유동자산 *= 1000000

        print('유동자산: %s' % (format(유동자산, ',')))

        # return 유동자산

        # 유동자산 대신 유보율 활용
        request_type_list = (
            creon.StockInfo.자본금_71,
            creon.StockInfo.유보율_76  # (잉여금/납입자본금) x 100%
        )
        info_list = stStockInfo.getInfoDetail(stock_name, request_type_list)

        print('  유보율: %s %%' % (info_list[1]))

        자본금 = info_list[0] * 1000000 # 자본금은 단위가 백만
        print('  자본금: %s' % (format(자본금, ',')))
        잉여금 = info_list[1] * 자본금 / 100
        print('  잉여금: %s' % (format(잉여금, ',')))

        if 유동자산 > 0:
            return 유동자산
        return 잉여금

    def get_TOTAL_DEBT(self, stock_name): # 총 부채 = 부채율 * 총자산
        # 총자산 = 주당순자산(BPS) * 상장주식 수
        stStockInfo = creon.StockInfo()
        request_type_list = (
            creon.StockInfo.총상장주식수_20,
            creon.StockInfo.부채비율_75,
            creon.StockInfo.BPS_89
        )
        info_list = stStockInfo.getInfo(stock_name, request_type_list)
        상장주식수 = info_list[0]
        부채비율 = info_list[1]
        주당순자산 = info_list[2] # BPS (Book-value Per Share)
        isBigListingStock = creon_98_stocks_by_industry.StocksByIndustry().isBigListingStock(stock_name)
        if isBigListingStock == True:
            상장주식수 *= 1000
        총자산 = 주당순자산 * 상장주식수
        # print('부채비율 : %s' % (부채비율))
        총부채 = (부채비율 / 100) * 총자산
        print('  총부채: %s' % (format(총부채, ',')))
        return 총부채

    # [참고] https://money2.creontrade.com/e5/mboard/ptype_basic/plusPDS/DW_Basic_Read.aspx?boardseq=299&seq=84&page=1&searchString=&prd=&lang=&p=8833&v=8639&m=9505
    def get_MARKET_CAPITALIZATION(self, stock_name): # 시가 총액 = 상장주식 수 * 현재가
        stStockInfo = creon.StockInfo()
        info_list = stStockInfo.getInfoDetail(stock_name)
        #     StockInfo.현재가_4,
        #     StockInfo.고가_6,
        #     StockInfo.거래량_10,
        #     StockInfo.거래대금_11,
        #     StockInfo.총상장주식수_20,
        #     StockInfo.전일종가_23,
        #     StockInfo.PER_67,
        #     StockInfo.BPS_89
        현재가 = info_list[0]
        # if stock_name == 'CJ':
            # 현재가 = 105643
            # 현재가 = 107000 # o
            # 현재가 = 108000 # o
            # 현재가 = 108500 # o
            # 현재가 = 108550 # o
            # 현재가 = 108580 # o
            # 현재가 = 108590 # x
            # 현재가 = 108600 # x
            # 현재가 = 108700 # x
            # 현재가 = 108800 # x
            # 현재가 = 109000 # x
            # 현재가 = 110000 # x
            # 현재가 = 120000 # x
        상장주식수 = info_list[4]

        # 상장주식수 20억 이상이면 1000 단위로 제공됨
        isBigListingStock = creon_98_stocks_by_industry.StocksByIndustry().isBigListingStock(stock_name)
        if isBigListingStock == True:
            상장주식수 *= 1000

        시가총액 = 현재가 * 상장주식수
        print('시가총액: %s' % (format(시가총액, ',')))
        return 시가총액

# NOTE: (minsik.son) for test
if __name__ == "__main__":
    # creon_0_Init.Connection().do_creon_forced_reconnect()

    if creon_0_Init.Connection().is_creon_connected() == False:
        creon_0_Init.Connection().do_creon_forced_reconnect()
    else:
        print('[CREON] already connected~')
    util = Quant_Utils()

    stock_list = (
        '삼성전자',
        'SK하이닉스',
        'CJ',
        '셀트리온',
        '금강공업',
        '아시아나항공',
        'NHN',
        '마니커'
    )
    print(stock_list)
    for i in stock_list:
        stock_name = i
        print('이름: %s' % (stock_name))
        구매여부 = util.NCAV(stock_name)
        print('구매여부: %s' % (구매여부))
        print('----------------------------')