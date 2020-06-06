import win32com.client

from . import utils

class StocksByIndustry:
    MARKET = {
        '코스피':1,
        '코스닥':2,
    }
    def __init__(self):
        self.instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

        self.stUtils = utils.Utils()
        
    def isBigListingStock(self, stock_name):
        # 상장주식수 20억 이상일 경우 return True
        stock_code = self.stUtils.get_code_from_name(stock_name)
        return self.instCpCodeMgr.IsBigListingStock(stock_code)

    def getStockListByMarket(self, market):
        __market = 0
        if 0 <= market | market <= 5:
            __market = market
        codeList = self.instCpCodeMgr.getStockListByMarket(__market)
        return codeList

    def 업종_별_코드_리스트(self, bPrint=False):
        industryCodeList = self.instCpCodeMgr.GetIndustryList()
        
        # industry name 출력
        if bPrint == True:
            for industryCode in industryCodeList:
                print("%s - %s" % (industryCode, self.instCpCodeMgr.GetIndustryName(industryCode)))

        return industryCodeList

    def 업종_내_종목_코드_리스트(self, 업종코드):
        targetCodeList = self.instCpCodeMgr.GetGroupCodeList(업종코드)
        for stockCode in targetCodeList:
            stockName = self.stUtils.get_name_from_code(stockCode)
            print(stockCode, stockName)

        return targetCodeList

