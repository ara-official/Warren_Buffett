import win32com.client
import pythoncom

import datetime # https://datascienceschool.net/view-notebook/465066ac92ef4da3b0aba32f76d9750a/
import time

from . import utils

TRUE = 1
FALSE = 0

# 1. 초기화 및 크레온 접속 ?
# 2. 조회
# 3. 알고리즘 (todo)
# 4. 매매/매수
# 5. 결과 확인 (== 조회?)
# (6. 그래프)

class Trading:
    
    BlockRequest_ReturnValue = {
        '정상요청':0,
        '통신요청실패':1,
        '그외의내부오류':3
    }

    매매 = {
        '매도':1,
        '매수':2
    }

    def __init__(self, logging=False):
        self.logging = logging

        self.stUtils = utils.Utils()

        self.instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")

        # 주식 잔고 조회
        self.instCpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

        # 주식 예약 정보 조회 (https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=291&seq=187&page=1&searchString=CpTdNew9061&p=&v=&m=)
        self.instCpTdNew9061 = win32com.client.Dispatch("CpTrade.CpTdNew9061")

        # 주식 취소
        self.instCpTd0314 = win32com.client.Dispatch("CpTrade.CpTd0314")

        
        self.상품관리구분코드 = {
            '주식':1,
            '선물/옵션':2,
            'EUREX':16,
            '해외선물':64,
        } # __상품관리구분코드['주식'] + __상품관리구분코드['선물/옵션'] 요런 식으로 사용 가능함
        self.stockAccount = ''
        self.stockAccountFlag = ''

    # 거래 관련부 : init -> setinputvalue -> blockrequest
    def do_trade_init(self):
        print('do_trade_init 1111111111111111')
        bInitResult = self.instCpTdUtil.TradeInit()
        print('do_trade_init 2222222222222222')

        bReturn = False
        if bInitResult == 0:
            if self.logging == True:
                print('[tradeInit] 성공')
            bReturn = True

            print('do_trade_init 333333333333')

            self.stockAccount = self.instCpTdUtil.AccountNumber[0]
            self.stockAccountFlag = self.instCpTdUtil.GoodsList(self.stockAccount, self.상품관리구분코드['주식']) # ?
        elif bInitResult == -1:
            print('[tradeInit] 오류')
        elif bInitResult == 1:
            print('[tradeInit] OTP/보안카드 키 입력 잘못 됨')
        elif bInitResult == 3:
            print('[tradeInit] 취소')
        else:
            print('[tradeInit] ??')
        return bReturn


    def 주식_주문(self, 매매, stockName, 주문단가, 주문수량, 주문호가구분코드='01', bPrint=False, bTest=False):
        SetInputValue_param = {
            '주문종류코드':0,
            '계좌번호':1,
            '상품관리구분코드':2,
            '종목코드':3,
            '주문수량':4,
            '주문단가':5,
            '주문조건구분코드':7,
            '주문호가구분코드':8,

            # 이하 생략
        }

        if ((매매 == 1) | (매매 == 2)) == False:
            print('[param] 매매 를 1(매도) 또는 2(매수)로 지정하세요')
            return

        if bPrint == True:
            print('__내_계좌_번호:', self.stockAccount)

        if bPrint == True:
            print(self.stockAccountFlag)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문종류코드'], 매매) # 1: 매도, 2: 매수
        self.instCpTd0311.SetInputValue(SetInputValue_param['계좌번호'], self.stockAccount)
        self.instCpTd0311.SetInputValue(SetInputValue_param['상품관리구분코드'], self.stockAccountFlag[0]) # 
        stockCode = self.stUtils.get_code_from_name(stockName)
        self.instCpTd0311.SetInputValue(SetInputValue_param['종목코드'], stockCode)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문수량'], 주문수량)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문단가'], 주문단가)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문조건구분코드'], '0') # '0' : 없음 [default]
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문호가구분코드'], 주문호가구분코드) # '01' : 보통 [default], '03': 시장가 ([참고] https://money2.creontrade.com/html/WTS/Customer/CWGuideUser/DW05_CUS_INF_001.html?m=2182&p=5457&v=4614#tabM1_2)

        __orderCode = 0
        # 요청
        if bTest == False:
            BlockRequest_result = self.instCpTd0311.BlockRequest()
            if BlockRequest_result == self.BlockRequest_ReturnValue['정상요청']:
                if 매매 == 1: # 매도
                    print('[주식_주문] result: 정상 요청 (%s 매도)' % (stockName))
                elif 매매 == 2: # 매수
                    print('[주식_주문] result: 정상 요청 (%s 매수)' % (stockName))
                __orderCode = self.instCpTd0311.GetHeaderValue(8) # 8:(long) 주문번호
                
            else:
                print('[주식_주문] result: 문제 발생 (%s)' % (BlockRequest_result))

        # 결과 조회 -> Subscribe 방식으로 확인 해야함
        
        return __orderCode

    def 주식_잔고_조회(self, bPrint=False):
        if bPrint == True:
            print('> 주식_잔고_조회')

        if bPrint == True:
            print('계좌번호 : %s, 주식상품_구분 : %s' % (self.stockAccount, self.stockAccountFlag))
        
        input_value_field = {
            '계좌번호': 0,
            '상품관리구분코드': 1,
            '요청건수': 2
        }
        self.instCpTd6033.SetInputValue(input_value_field['계좌번호'], self.stockAccount)  # 계좌번호
        self.instCpTd6033.SetInputValue(input_value_field['상품관리구분코드'], self.stockAccountFlag[0])  # 상품구분 - 주식 상품 중 첫번째
        self.instCpTd6033.SetInputValue(input_value_field['요청건수'], 50)  # 요청 건수(최대 50)
        # self.dicflag1 = {ord(' '): '현금',
        #                  ord('Y'): '융자',
        #                  ord('D'): '대주',
        #                  ord('B'): '담보',
        #                  ord('M'): '매입담보',
        #                  ord('P'): '플러스론',
        #                  ord('I'): '자기융자',
        #                  }

        return self.requestJango(bPrint)

    def requestJango(self, bPrint=False):
        while True:
            self.instCpTd6033.BlockRequest()

            # 통신 및 통신 에러 처리
            rqStatus = self.instCpTd6033.GetDibStatus()
            rqRet = self.instCpTd6033.GetDibMsg1()
            if bPrint == True:
                print("통신상태", rqStatus, rqRet)
            if rqStatus != 0:
                print("통신상태", rqStatus, rqRet)
                return False
 
            header_value_field = {
                '수신개수': 7
            }
            cnt = self.instCpTd6033.GetHeaderValue(header_value_field['수신개수'])

            if bPrint == True:
                print(cnt)
 
            잔고 = 0
            ret_item_list = []
            for i in range(cnt):
                item = {}
                code = self.instCpTd6033.GetDataValue(12, i)  # 종목코드
                item['종목코드'] = code
                item['종목명'] = self.instCpTd6033.GetDataValue(0, i)  # 종목명
                item['잔고수량'] = self.instCpTd6033.GetDataValue(7, i)  # 체결잔고수량
                item['매도가능'] = self.instCpTd6033.GetDataValue(15, i)
                item['장부가'] = self.instCpTd6033.GetDataValue(17, i)  # 체결장부단가
                item['매입금액'] = item['장부가'] * item['잔고수량']
                __n_days_list = self.stUtils.get_stock_value_n_days(code, 1) # parameter 가 1이 아닐 경우, 아래 code 수정 필요
                item['현재가'] = __n_days_list[0][2] # 시가
                item['대비'] = 0
                item['거래량'] = 0

                # 추가한 정보
                item['손익단가'] = self.instCpTd6033.GetDataValue(18, i)
                item['평가손익'] = self.instCpTd6033.GetDataValue(10, i)
                item['수익률'] = self.instCpTd6033.GetDataValue(11, i)
                item['평가금액'] = self.instCpTd6033.GetDataValue(9, i)

 
                합계 = item['잔고수량'] * item['현재가']
                if bPrint == True:
                    print('%s : 잔고수량(%s) * 현재가(%s) = (%s) (매도가능? %s)' % (item['종목명'], item['잔고수량'], item['현재가'], 합계, item['매도가능']))
                잔고 = 잔고 + 합계
                ret_item_list.append(item)

            if bPrint == True:
                print('잔고 : %s' % format(잔고, ','))
            if self.instCpTd6033.Continue == False: # README.md 의 '3. RQ/RP 의 연속 data 통신' 참고
                break
        return ret_item_list

    def 주식_주문_취소(self, 원주문번호, 종목이름, 취소수량=0, bPrint=False):
        if bPrint == True:
            print('> 주식_주문_취소 (원주문번호: %s, 종목이름: %s, 취소수량: %s)' % (원주문번호, 종목이름, 취소수량))

        __SetInputValue_param = {
            '원주문번호': 1,
            '계좌번호': 2,
            '상품관리구분코드': 3,
            '종목코드': 4,
            '취소수량': 5, # 0 입력하면 잔량 전부
        }
        if bPrint == True:
            print('   > 계좌: %s, 주식상품_구분: %s' % (self.stockAccount, self.stockAccountFlag))

        self.instCpTd0314.SetInputValue(__SetInputValue_param['원주문번호'], 원주문번호)
        self.instCpTd0314.SetInputValue(__SetInputValue_param['계좌번호'], self.stockAccount)
        self.instCpTd0314.SetInputValue(__SetInputValue_param['상품관리구분코드'], self.stockAccountFlag[0])
        self.instCpTd0314.SetInputValue(__SetInputValue_param['종목코드'], self.stUtils.get_code_from_name(종목이름))
        self.instCpTd0314.SetInputValue(__SetInputValue_param['취소수량'], 취소수량)

        ret = self.instCpTd0314.BlockRequest()
        print('ret : %s' % (ret))

        print("[주식_주문_취소] 주문결과", self.instCpTd0314.GetDibStatus(), self.instCpTd0314.GetDibMsg1())
        if self.instCpTd0314.GetDibStatus() != 0:
            return False
        return True


    def 주식_주문_두번째방법(self, 매매, 종목코드, bPrint=False):
        if bPrint == True:
            print('> 주식_주문_조회')

        if bPrint == True:
            print('계좌번호 : %s, 주식상품_구분 : %s' % (self.stockAccount, self.stockAccountFlag))
        
        input_value_field = {
            '계좌번호': 0,
            '상품관리구분코드': 1,
            '주문종류코드': 2,
            '종목코드': 3,

        }
        self.instCpTdNew9061.SetInputValue(input_value_field['계좌번호'], self.stockAccount)  # 계좌번호
        self.instCpTdNew9061.SetInputValue(input_value_field['상품관리구분코드'], self.stockAccountFlag[0])  # 상품구분 - 주식 상품 중 첫번째
        self.instCpTdNew9061.SetInputValue(input_value_field['주문종류코드'], 매매)  # 주문종류코드 - 1: 매도, 2: 매수)
        self.instCpTdNew9061.SetInputValue(input_value_field['종목코드'], 종목코드)  # 주문종류코드 - 1: 매도, 2: 매수)


        # self.instCpTdNew9061

class StockInfo:
    현재가_4 = 4 
    고가_6 = 6
    매수호가_9 = 9
    거래량_10 = 10          # **
    거래대금_11 = 11
    종목명_17 = 17
    총상장주식수_20 = 20
    전일거래량_22 = 22      # **
    전일종가_23 = 23
    PER_67 = 67             # ** 주가/주당순이익
    액면가_72 = 72
    부채비율_75 = 75        # ** 대차대조표의 부채 총액을 자기자본으로 나눈 비율
    자기자본이익률_77 = 77  # **
    매출액증가율_78 = 78    # **
    순이익증가율_80 = 80    # **
    BPS_89 = 89            # **s 주당순자산

    def __init__(self):
        self.stUtils = utils.Utils()

        self.instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

    def getRequestTypeListBrief(self):
        request_type_list = (
            StockInfo.현재가_4,
            StockInfo.거래량_10,
            StockInfo.PER_67,
            StockInfo.BPS_89
        )
        return request_type_list

    def printRequestTypeListBrief(self, result):
        print(
            '    >',
            '현재가:'  , format(result[0], ','), '원 |',
            '거래량:'  , format(result[1], ','), '회 |',
            'PER:'    , format(round(result[2], 2), ','), '배 |',
            'BPS:'    , format(result[3], ','), '원',
        )

    def getRequestTypeListDetailed(self):
        request_type_list = (
            StockInfo.현재가_4,
            StockInfo.고가_6,
            StockInfo.거래량_10,
            StockInfo.거래대금_11,
            StockInfo.총상장주식수_20,
            StockInfo.전일종가_23,
            StockInfo.PER_67,
            StockInfo.BPS_89
        )
        return request_type_list

    def printRequestTypeListDetailed(self, result):
        print(
            '    >',
            '현재가:'  , format(result[0], ','), '원 |',
            '고가:'    , format(result[1], ','), '원 |',
            '거래량:'  , format(result[2], ','), '회 |',
            '거래대금:', format(result[3], ','), '원 |',
            '총상장주식수', format(result[4], ','), '개 |',
            '전일종가', format(result[5], ','), '원 |',
            'PER:'    , format(round(result[6], 2), ','), '배 |',
            'BPS:'    , format(result[7], ','), '원',
        )

    

    def getInfo(self, stockName, requestType):
        필드_요청타입 = 0
        필드_주식코드 = 1
        # print('requestType : %s' % (requestType))
        self.instMarketEye.SetInputValue(필드_요청타입, requestType)
        주식코드 = self.stUtils.get_code_from_name(stockName)
        self.instMarketEye.SetInputValue(필드_주식코드, 주식코드)

        self.instMarketEye.BlockRequest() # 서버에 데이터 요청

        ret_value = []
        if type(requestType) == int:
            ret_value.append(self.instMarketEye.GetDataValue(0, 0))
        else :
            for i in range(len(requestType)):
                ret_value.append(self.instMarketEye.GetDataValue(i, 0))

        return ret_value

    def getInfoSimple(self, stockName, bPrint=False):
        request_result_list = self.getInfo(stockName, self.getRequestTypeListBrief())
        if bPrint == True:
            self.printRequestTypeListBrief(request_result_list)
        return request_result_list

    def getInfoDetail(self, stockName, bPrint=False):
        request_result_list = self.getInfo(stockName, self.getRequestTypeListDetailed())
        if bPrint == True:
            self.printRequestTypeListDetailed(request_result_list)
        return request_result_list

    def stockVolumeAnalysis(self, stockName, 몇배수, 비교기간=60, bPrint=False):
        __stockCode = self.stUtils.get_code_from_name(stockName)
        __거래량 = 8
        self.stUtils.set_stock_chart_info_and_request(__stockCode, ord('2'), 비교기간, __거래량,  ord('D'), ord('1'))

        # server 에서 data 받아옴
        volumes = []
        __수신개수 = 3
        __numData = self.stUtils.instStockChart.GetHeaderValue(__수신개수) # 비교기간 이랑 같을 듯.

        __종목코드 = 0
        for i in range(__numData):
            volume = self.stUtils.instStockChart.GetDataValue(__종목코드, i)
            if volume == 0:
                #print('%s 은(는) 거래가 중지된 품목입니다.' % (stockName))
                return # 거래 중지된 경우
            volumes.append(volume)
            # print('volumes[%s] : %s' % (i, volumes[i]))
        # print(volumes)

        volumesLen = len(volumes)
        if volumesLen == 1:
            avgVolume = volumes[0]
        else :
            avgVolume = (sum(volumes) - volumes[0]) / (len(volumes) - 1)

        # print('  > volumes[0] : %s' % (volumes[0]))
        # print('  > avgVolume : %s' % (avgVolume))
        if volumes[0] > avgVolume * 몇배수:
            __거래량_배수 = round((volumes[0] / avgVolume), 3)
            if bPrint == True:
                print('(거래량 %s 배) %s 은(는) 대박 주! ' % (__거래량_배수, stockName))
            return __거래량_배수
        else:
            return 0
            #print('(거래량 %s 배) %s 은(는) 일반 주.. ' % (round((volumes[0] / avgVolume), 3), stockName))

