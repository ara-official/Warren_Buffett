import os
import sys
<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
# creon_99_algorithm.py __main__ 으로 실행 하려면, path 를 일일이 추가 해야함..
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

=======
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py

from time import sleep

# https://blog.doosikbae.com/52
from util import utils
from util import creon
from util import creon_0_Init
from util import creon_1_SB_PB
from util import creon_98_stocks_by_industry
from util import login
<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py

from data_process import json_utils
from data_process import log

from pythoncom import PumpWaitingMessages

=======
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py

class Algorithm:
    매수_목록_0220_이전 = (
        ''
    )
    #TODO: JSON 치환.
    매수_목록_0220 = (
        # '이더블유케이', # 1.06%
        '파인테크닉스',
        # '신스타임즈', # 1.24%
        # 'APS홀딩스',
        # '제일바이오',
        # '인프라웨어', # 2 주: +1.17%
        # '에이치엘비파워', # 2 주: +1.06%
        # '아이씨디', # -6.48%
    )

    # 매수_목록_0224 = (
    #     # '창해에탄올',
    #     # '진양제약',
    #     # '메디앙스',
    #     # '고려제약',
    #     # '대림제지',
    # )

    매수_목록_0226 = (
        # '오공', # 1.1%
        # '바른손이앤에이', # -5.14%
    )

    매수_목록_0227 = (
<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
        # '스타모빌리티',
        # '한류AI센터',
=======
        '스타모빌리티',
        '한류AI센터',
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py
        # '아이씨디', # -3.49%
        # '국일제지', # -3.28%
        # '엘앤씨바이오'# -3.36%
    )

    매수_목록_0228 = (
<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
        # '스타모빌리티', # 1
        # '한류AI센터', # 2
        # '두올산업',
        # '셀리버리',
        # '대창솔루션',
    )

    매수_목록_0302 = (
        # '큐브엔터',
        # '대창솔루션',
        '두올산업',
        # '한류AI센터',
        # '알리코제약'
    )
    
    current_purchase_stock_list = ()
    current_purchase_stock_list += 매수_목록_0220
    # current_purchase_stock_list += 매수_목록_0224
    # current_purchase_stock_list += 매수_목록_0226
    current_purchase_stock_list += 매수_목록_0227
    current_purchase_stock_list += 매수_목록_0228
    current_purchase_stock_list += 매수_목록_0302

    def __init__(self):

=======
        '스타모빌리티', # 1
        '한류AI센터', # 2
        '두올산업',
        '셀리버리',
        '대창솔루션',
    )
    
    기존_매수_목록 = ()
    기존_매수_목록 += 매수_목록_0220
    # 기존_매수_목록 += 매수_목록_0224
    # 기존_매수_목록 += 매수_목록_0226
    기존_매수_목록 += 매수_목록_0227

    def __init__(self):
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py
        self.stInit = creon_0_Init.Connection()

        self.stUtils = utils.Utils()
        self.stStockByIndustry = creon_98_stocks_by_industry.StocksByIndustry()

        self.stStockInfo = creon.StockInfo()

        self.stTrading = creon.Trading(logging=True)

# 적중 횟수 측정 (count) -> 기업들이 여러개
# 적중 횟수 / 수집 기간 => (%) 높은 ~ 낮은
# algorithm_3 : "금일 고가 > 전일 종가" 인 횟수를 counting
# 세금 : 매수, 매도 ==> 그냥 0.3 % 정도라고 생각하면 됨...
# "종가 < 다음날 고가" 비교할 때, 수수료도 포함 시켜야 더 정확하겠다.
    def algorithm_3__stock_purchase_recommandation(self, 전체기간=10, marketType='코스닥', top=5, 기대수익률=2, 비교횟수=5, bPrint=False, comparison_period=2000):
        __bPrint = bPrint

        if self.stTrading.do_trade_init() == True:
            추천_종목_리스트 = []
            추천_종목_이름_리스트 = []
            투자_후보_예상수익 = []

            if marketType == '코스피':
                __markeyType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피']
            elif marketType == '코스닥':
                __markeyType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스닥']
            else:
                __markeyType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스닥']

            stock_code_list = self.stStockByIndustry.getStockListByMarket(__markeyType)
            # stock_code_list = stock_code_list[110:150]

            # '네이처셀', '코센', '유니크', '원풍물산', '대한광통신'
            # stock_code_list = []
            # stock_code_list.append(self.stUtils.get_code_from_name('네이처셀'))
            # stock_code_list.append(self.stUtils.get_code_from_name('코센'))
            # stock_code_list.append(self.stUtils.get_code_from_name('유니크'))
            # stock_code_list.append(self.stUtils.get_code_from_name('원풍물산'))
            # stock_code_list.append(self.stUtils.get_code_from_name('대한광통신'))

            # stock_code_list = self.stStockByIndustry.getStockListByMarket(1)
            # stock_code_list += (self.stStockByIndustry.getStockListByMarket(2))
            stock_name_list = self.stUtils.get_nameList_from_codeList(stock_code_list)
            
            # stock_name_list = self.후보군_종목_리스트
            # stock_code_list = self.stUtils.get_codeList_from_nameList(stock_name_list)

            if bPrint == True:
                print(stock_code_list)
                print(stock_name_list)

            날짜 = utils.Utils.InputValue_StockChart_Field_type['날짜']
            고가 = utils.Utils.InputValue_StockChart_Field_type['고가']
            종가 = utils.Utils.InputValue_StockChart_Field_type['종가']


            #TODO:기대수익률 JSON으로 변경
            if bPrint == True:
                print('기대수익률:', 기대수익률)
            result_list = []
            for j in range(len(stock_code_list)):
                item = {}
                item['종목명'] = stock_name_list[j]
                item['종목코드'] = stock_code_list[j]
                item['정보'] = self.stUtils.get_stock_value_n_days(stock_code_list[j], comparison_period)
                result_list.append(item)
                
            # for j in range(len(result_list)):
            #     print(result_list[j])

            ###################################################################################
            # 계산식 잘못 된 부분 있을거 같은데, 찾자!
            ############ 금일 고가로 계산하는게 아니라, % 로 계산해야 한다..! (수정함)
            ############ "(n-2) 종가 ==> (n-1) 고가" 를 활용해 n 종가에 구매해서 n + 1 에 팔도록 해야 한다...
            ###################################################################################

            ###########################################
            ## 비교기간만 바꿔봤을 때, 수익
            # CREON API response time 때문에, 우선 "삼륭물삼 ~ 에이치엘비생명과학" 만 비교
            
            __비교기간 = 비교횟수
            #TODO:__비교기간 값 JSON으로 넘겨주기
            # __비교기간 = 1 # 3754
            # __비교기간 = 2 # 5093 # BEST
            # __비교기간 = 3 # 4410
            # __비교기간 = 5 # 4333
            # __비교기간 = 10 # 4232
            # __비교기간 = 50 # 1814
            # __비교기간 = 100 # -102

            ## 뭔가 구멍이 있는듯?
            ###########################################

#######################################################
# Simulator
#######################################################

            #TODO:전체기간 값 JSON으로 넘겨주기
            __전체기간 = 전체기간 # 2주
            __전체수익 = 0
            __종목별_매매_수량 = 1 # top 5 각 1 주씩 매수
            bFirst = 0
            for __오늘부터며칠전 in range(1, __전체기간+1):
                __추천_종목_리스트, __수익_리스트 = self.기간_별_추천_종목(result_list, __오늘부터며칠전, __비교기간, 최고수익=False, 수익률=기대수익률, top=top, bPrint=__bPrint, bPrintDetail=False)
                
                __매수비용 = 0
                __하루수익 = 0
                __추천_종목_이름_리스트 = []
                for i in range(len(__수익_리스트)):
                    ################################################
                    # [중요] 세금 적용이 되지 않았습니다!!!!!!!!!!!!!
                    ################################################

                    __매수비용 += __추천_종목_리스트[i]['정보'][__오늘부터며칠전 + 1][종가] * __종목별_매매_수량
                    __하루수익 += __수익_리스트[i] * __종목별_매매_수량
                    __추천_종목_이름_리스트.append(__추천_종목_리스트[i]['종목명'])
                if bPrint == True:
                    print('[%s일전]** 수익: %6s (매수비용: %s), 수익_리스트: %s [%s] ' % (__오늘부터며칠전, __하루수익, __매수비용, __수익_리스트, __추천_종목_이름_리스트))
                __전체수익 += __하루수익
                # for i in range(len(__추천_종목_리스트)):
                #     print('(%2s/%2s) %s' % (__추천_종목_리스트[i]['성공횟수'], __비교기간, __추천_종목_리스트[i]['종목명']))

                # 오늘 기준으로 매수할 종목 추천
                if bFirst == 0:
                    추천_종목_리스트 = __추천_종목_리스트
                    추천_종목_이름_리스트 = __추천_종목_이름_리스트
                    투자_후보_예상수익 = __수익_리스트
                    bFirst = 1

            if bPrint == True:
                print('>> 전체수익: %s' % (round(__전체수익, 2)))
            return 추천_종목_리스트, 추천_종목_이름_리스트, 투자_후보_예상수익

# nm
# n + 2(m - 1) = n + m
# m : 전체기간 ( 100 )
# n : 비교기간 ( 10 )
# n + 2(m - 1) = n + m
# n + 2(m - 1) = n + 2m - 2 = n + m
# 
# nm
# 
#   
# nm => n + m = >
#           
    def 기간_별_추천_종목(self, stock_info_list, 오늘로부터며칠전, 비교기간, 최고수익=False, 수익률=2, top=5, bPrint=False, bPrintDetail=False):
        if bPrint == True:
            print('##############################################################')
        __추천_종목_리스트 = []

        날짜 = utils.Utils.InputValue_StockChart_Field_type['날짜']
        고가 = utils.Utils.InputValue_StockChart_Field_type['고가']
        종가 = utils.Utils.InputValue_StockChart_Field_type['종가']

        if bPrint == True:
            print('> [오늘: %s]' % (self.stUtils.현재_시간()))
            print('> 오늘로부터며칠전: %s, 비교기간: %s' % (오늘로부터며칠전, 비교기간))
        for i in range(len(stock_info_list)):
            item = stock_info_list[i] # 종목 정보
            유효기간 = len(item['정보'])
            
            __목표_수익_달성_횟수 = 0
            __성공여부 = '>'
            for j in range(오늘로부터며칠전, 오늘로부터며칠전+비교기간):
                if 유효기간 > 오늘로부터며칠전+비교기간:
                    # (n-1)일 종가와, (n)일 고가 비교
                    if item['정보'][j][고가] > item['정보'][j+1][종가]:
                        __수익 = item['정보'][j][고가] - item['정보'][j+1][종가]
                        if __수익 > (item['정보'][j+1][종가] * (수익률 / 100)):
                            __목표_수익_달성_횟수 += 1
                            __성공여부 = '>'
                        else:
                            __성공여부 = '<'
                    else:
                        __성공여부 = '<'
                        # item['종목명']
                        # item['종목코드']
                        # item['정보']

                    if (bPrint == True) & (bPrintDetail == True):
                        print('[%s 고가:%s] %s [%s 종가:%s] <종목명: %s>'
                            % (
                                item['정보'][j][날짜], item['정보'][j][고가],
                                __성공여부,
                                item['정보'][j+1][날짜], item['정보'][j+1][종가],
                                item['종목명']
                            )
                        )
            if bPrint == True:
                print('__목표_수익_달성_횟수: (%3s/%3s) <종목명: %s>' % (__목표_수익_달성_횟수, 비교기간, item['종목명']))
            item['성공횟수'] = __목표_수익_달성_횟수
            __추천_종목_리스트.append(item)

        # sorting
        __추천_종목_리스트 = sorted(__추천_종목_리스트, key=lambda item:item['성공횟수'], reverse=True)

        
        # 수익 정보
        __수익_리스트 = []
        for i in range(0, top):
            __매도날_고가 = __추천_종목_리스트[i]['정보'][오늘로부터며칠전][고가]
            __매도날_종가 = __추천_종목_리스트[i]['정보'][오늘로부터며칠전][종가]
            __매수날_종가 = __추천_종목_리스트[i]['정보'][오늘로부터며칠전+1][종가]
            __수익 = __매도날_고가 - __매수날_종가
            if __수익 >= (__매수날_종가 * (수익률 / 100)):
                if 최고수익 == False:
                    __수익 = __매수날_종가 * (수익률 / 100)
            else:
                # 매도날 종가에 팔고, 새로 계산된 top 5 를 구매....
                __수익 = __매도날_종가 - __매수날_종가

            __수익_리스트.append(__수익)

        if bPrint == True:
            print('##############################################################')
        return __추천_종목_리스트, __수익_리스트


# 시나리오
# 장 중인지 확인
# >> [1] 장 열릴 때까지 대기
# 장 열림!
# >> 어제 매수한 종목 있으면, 수익률(ex. 2%) 에 맞춰 매도 걸어놓음
# >>> 매도 시, 가격 최소 단위? 맞춰서 매도 걸어야 함.;;
# 목표 수익률에 매도 등록
# 매도 완료 시 장 마감 2분 전까지 sleep
# 장 마감 1분 전, 현재 주가로 1 주 매수
# >> 장 마감 1분 전인지 확인 (1분 이상 남았다면 대기)
# >> 매수 종목 정보 검색
# >> 매수 수행
# >>> (optional) 실시간 주가 subscribe
# >>> 매수 성공 확인
# >>> 모든 subscribe 해제
# (처음으로 돌아가서 반복) <-- x

<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py

## 알고리즘 단순화
# [1] 크레온 접속
# [2] 어제 종가 종목            => 오늘 고가 매도
# [3] 종목 추천 알고리즘 수행
# [4] 어제 종가 종목 (매도 실패) => 오늘 종가 매도
# [5] 추천된 종목               => 오늘 종가 구매

    def algorithm_4__buy_yesterday_low_price__sell_today_high_price(self):
        __기대수익률 = 1.1 # %
=======
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py

## 알고리즘 단순화
# [1] 크레온 접속
# [2] 어제 종가 종목            => 오늘 고가 매도
# [3] 종목 추천 알고리즘 수행
# [4] 어제 종가 종목 (매도 실패) => 오늘 종가 매도
# [5] 추천된 종목               => 오늘 종가 구매

    def algorithm_4__buy_yesterday_low_price__sell_today_high_price(self):
##########
        __기대수익률 = 1.1 # %

        __bDBG = True

        __bExit = False
        __bIsStockMarketOpen = False

        __time_table = {
            ''
        }

        # hard coding
        매도_원주문_번호_리스트 = []
        매도_종목_리스트 = [] # 원주문번호랑 매도 종목이랑 matching 하기위해 사용.

        __stCpStockConclusion = creon_1_SB_PB.CpPBConclusion()

        while True:
            print('******************************************!!!!!!')
# 장 중인지 확인
            __bIsStockMarketOpen = self.stUtils.장_중인지_확인()
<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
            connect = self.stInit.is_creon_connected_as_admin() # NOTE: always return True.
=======
            connect = self.stInit.do_creon_forced_reconnect() # NOTE: always return True.
            # creon_0_Init.Connection().kill_creon()
            # connect = creon_0_Init.Connection().run_creon(login.id, login.pwd, login.pwdcert) 
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py
            if __bDBG == True:
                __bIsStockMarketOpen = True
                print('__bIsStockMarketOpen: %s, connect: %s' % (__bIsStockMarketOpen, connect))

# >> [1] 장 열릴 때까지 대기
            if (connect == False) | (__bIsStockMarketOpen == False):
                print('# >> [1] 장 열릴 때까지 대기')
                while True:
                    sleep(5)
                    # connect = self.stInit.do_creon_connect() # NOTE: always return True. 

                    print('현재 시간 : %s' % (self.stUtils.현재_시간()))
                    if self.stUtils.장_중인지_확인() == True:
                        print('주식 장 시작!!!!!!!!!!!!!!!!!!!')
                        break
            else:                
# 장 열림!
                print('# [2] 장 열림!')
                # sleep(30) # 바로 시작하면, 계쏙 "크레온 보안카드 비밀번호 입력" 요청 하는 듯?
                bTradeInit = self.stTrading.do_trade_init()
                if bTradeInit == False:
                    exit()
# >> 어제 매수한 종목 있으면, 수익률(ex. 2%) 에 맞춰 매도 걸어놓음
# >>> 매도 시, 가격 최소 단위? 맞춰서 매도 걸어야 함.;;


                return connect # for DBG

                
                # 잔고 확인 (보유 주식)
                주식_잔고_리스트 = self.stTrading.주식_잔고_조회(bPrint=False)

<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
                #NOTE: *.json 에서 구매 목록 가져오도록 수정 필요
                # json_utils.json_write('purchase_list_0301.json', 'test', Algorithm.current_purchase_stock_list)
                # test = json_utils.json_read('purchase_list_0301.json', 'test')

=======
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py
                # 매수_목록_0218
                # 매수_목록_0220 로 갈아끼우자,
                # 매도 <-- 어제 매수한 종목에 대한 매도 주문

                __subscribe_code_list = []
                for i in range(len(self.current_purchase_stock_list)):
                    __code = self.stUtils.get_code_from_name(self.current_purchase_stock_list[i])
                    __subscribe_code_list.append(__code)
                __stCpStockConclusion.subscribe(__subscribe_code_list, __stCpStockConclusion)
                
                for i in range(len(주식_잔고_리스트)):
                    for j in range(len(self.current_purchase_stock_list)):
                        if 주식_잔고_리스트[i]['종목명'] == self.current_purchase_stock_list[j] :
                            __주문수량 = 1
                            # 매도 수행
                            # if (self.current_purchase_stock_list[j] == '인프라웨어') | (self.current_purchase_stock_list[j] == '에이치엘비파워'):
                            #     __주문수량 = 2

                            __매도_원주문번호 = self.stTrading.주식_주문( # *** 매수/매도 주문은 정상 동작함
                                매매 = 1, # 1: 매도, 2: 매수
                                stockName=self.current_purchase_stock_list[j],
                                주문단가=self.stUtils.get_trade_price((주식_잔고_리스트[i]['손익단가'] * (1 + (__기대수익률/100)))), # 손익단가 * 1.02 == 2 % 높게 매도
                                # 주문 단가 자리 수 맞춰야 함.
                                주문수량=__주문수량,
                                bPrint=False,
                                bTest=False
                            )
                            if __매도_원주문번호 != 0: # 0: 매도 주문 실패
                                매도_원주문_번호_리스트.append(__매도_원주문번호)
                                매도_종목_리스트.append(self.current_purchase_stock_list[j])
                print('매도_원주문_번호_리스트: %s' % (매도_원주문_번호_리스트))

                __bCalculate = False
                if __bDBG == True:
                    __bCalculate = True
                __계산_타이밍 = 1800 # 장 마감 30 분 전에 계산
                while __bCalculate == False:
                    __마감까지_남은시간 = self.stUtils.마감_까지_남은_시간().total_seconds()
                    __bCalculate = (__마감까지_남은시간 <= __계산_타이밍) # 장 중이지 않을 경우, __마감까지_남은시간 는 음수
                    # if __bDBG == True:
                    #     __bBuyStock = True

                    __log = '장 마감까지 %s 초 남음 (%s) (계산 타이밍: %s 초 전)' % (round(__마감까지_남은시간, 2), __bCalculate, __계산_타이밍)
                    print(__log)
                    # log.log_write(__log)
                    sleep(5)

# 장 마감? 1분 전, 현재 주가로 1 주 씩 매수 # 이 것도 딜레이 걸어야 함..
                __top = 5 # 5 개 회사 추천

                print('현재 시간 : %s' % (self.stUtils.현재_시간()))
                __추천_종목_리스트, __투자_후보_이름, __투자_후보_예상수익 = self.algorithm_3__stock_purchase_recommandation(전체기간=1, marketType='코스닥', top=__top, 기대수익률=__기대수익률, 비교횟수=100, bPrint=False) # marketType(0: 코스피, 1: 코스닥)
                print('현재 시간 : %s' % (self.stUtils.현재_시간()))
                
                print('** 추천 종목:', __투자_후보_이름, __투자_후보_예상수익)

# >> 장 마감 1분 전인지 확인 (1분 이상 남았다면 대기)
                # sleep(2)
                __투자_후보_현재_정보_리스트 = []
                __bBuyStock = False
                if __bDBG == True:
                    __bBuyStock = True
                # 0 원에 걸면? -> 바로 사지거나 팔릴 수 있음
                __매수_타이밍 = 240 # 2 분 30 초 전,,
                while __bBuyStock == False:
                    __마감까지_남은시간 = self.stUtils.마감_까지_남은_시간().total_seconds()
                    __bBuyStock = (__마감까지_남은시간 <= __매수_타이밍) # 장 중이지 않을 경우, __마감까지_남은시간 는 음수
                    # if __bDBG == True:
                    #     __bBuyStock = True

                    print('장 마감까지 %s 초 남음 (%s) (매수 타이밍: %s 초 전)' % (round(__마감까지_남은시간, 2), __bBuyStock, __매수_타이밍))
                    sleep(2)
                    
# 매도 실패에 대한 예외처리 필요.
                print('******************매도 실패에 대한 예외 처리******************')
                # 현재가로 매도 필요한 종목 목록..!
                for i in range(len(매도_종목_리스트)):
                    __stockConclusion = False # TODO: need to fix
                    print('__stockConclusion: %s' % (__stockConclusion))
                    if __stockConclusion == False: # 매도 안된 경우
                        # [TODO] 매도 주문 취소
                        # 기존 매도 주문 일괄 취소
                        __종목명 = self.current_purchase_stock_list[i]

                        # def 주식_주문_취소(self, 원주문번호, 종목이름, 취소수량=0, bPrint=False):
                        self.stTrading.주식_주문_취소(
                            원주문번호=매도_원주문_번호_리스트[i], # 원래 다 0 인지 확인 필요
                            종목이름=매도_종목_리스트[i], # 원주문번호랑 매도 종목이랑 순서 맞춰져 있음
                            취소수량=0, # 0: 전부
                            bPrint=True)

                        sleep(1) # 혹시 몰라서 delay
                        ## 현재가 매도 주문
                        print(__종목명)
                        __stockInfo = self.stStockInfo.getInfoDetail(__종목명, bPrint=True)
                        __현재가 = __stockInfo[0]

                        __주문수량 = 1
                        # if (__종목명 == '인프라웨어') | (__종목명 == '에이치엘비파워'):
                        #     __주문수량 = 2

                        self.stTrading.주식_주문( # *** 매수/매도 주문은 정상 동작함
                            매매 = 1, # 1: 매도, 2: 매수
                            stockName=__종목명,
                            # 주문단가=self.stUtils.get_trade_price(__현재가, 호가=-5),
                            주문단가=__현재가,
                            주문수량=__주문수량, # 0 이라고 전량 아님,,!!
                            주문호가구분코드='03', # 시장가로 매도
                            bPrint=False,
                            bTest=False)
                print('************************************************************************')

# >> 매수 종목 정보 검색
                for i in range(len(__투자_후보_이름)):
                    print(__투자_후보_이름[i])
                    __투자_후보_현재_정보_리스트.append(self.stStockInfo.getInfoDetail(__투자_후보_이름[i], bPrint=True)) # 출력되는 정보 순서 참고. 추후 dictionary 로 변경하면 좋을 듯,
                
                __매수_타이밍 = 60 # 1 분 0 초 전,,
                while __bBuyStock == False:
                    __마감까지_남은시간 = self.stUtils.마감_까지_남은_시간().total_seconds()
                    __bBuyStock = (__마감까지_남은시간 <= __매수_타이밍) # 장 중이지 않을 경우, __마감까지_남은시간 는 음수
                    # if __bDBG == True:
                    #     __bBuyStock = True

<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
                    __log = '장 마감까지 %s 초 남음 (%s) (매수 타이밍: %s 초 전)' % (round(__마감까지_남은시간, 2), __bBuyStock, __매수_타이밍)
                    print(__log)
                    # log.log_write(__log)
                    sleep(5)
=======
                    print('장 마감까지 %s 초 남음 (%s) (매수 타이밍: %s 초 전)' % (round(__마감까지_남은시간, 2), __bBuyStock, __매수_타이밍))
                    sleep(2)
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py
# >> 매수 수행
                if bTradeInit == True:
# >>> (optional) 실시간 주가 subscribe
                    # subscribe_stockcur_list = []
                    # for i in range(len(__투자_후보_이름)):
                    #     __stCpStockCur = creon_1_SB_PB.CpPBStockCur() # 실시간 주가 변동 확인 위해서 사용 *************** 현재 가격 받아오는건 정상동작 안함..
                    #     __code = self.stUtils.get_code_from_name(__투자_후보_이름[i])
                    #     __stCpStockCur.subscribe(__code, __stCpStockCur) # 실시간 거래 가능시간 이외에는, 현재가 고정이기 때문에 subscribe 해도 받는(receive)게 없다.
                    #     subscribe_stockcur_list.append(__stCpStockCur)

                    for i in range(len(__투자_후보_이름)):
                        __code = self.stUtils.get_code_from_name(__투자_후보_이름[i])
                        __stCpStockConclusion.subscribe(__code, __stCpStockConclusion)

                        __현재가 = __투자_후보_현재_정보_리스트[i][0]
                        self.stTrading.주식_주문( # *** 매수 주문은 정상 동작함
                            매매 = 2, # 2: 매수
                            stockName=__투자_후보_이름[i],
                            # 주문단가=self.stUtils.get_trade_price(__투자_후보_현재_정보_리스트[i][0], 호가=+5), # 현재가 ** 높은 가격 걸면?
                            주문단가=__현재가, # 현재가 ** 높은 가격 걸면?
                            주문수량=1,
                            주문호가구분코드='03', # 시장가로 매수
                            bPrint=False,
                            bTest=False
                        )
                
                    __bBuyComplete = False
                    __bSellComplete = False
# >>> 매수 성공 확인
                    __timeout = 100
                    __timeout_count = 0
                    while True:
                        PumpWaitingMessages() # https://ko.wikipedia.org/wiki/이벤트_루프
                        sleep(2)
                        if __stCpStockConclusion.get_buy_count() == len(__투자_후보_이름):
                            __bBuyComplete = True
                        if __stCpStockConclusion.get_sell_count() == len(self.current_purchase_stock_list):
                            __bSellComplete = True

                        print('[%s]' % (self.stUtils.현재_시간()))
                        __log = '매도 (%s/%s), 매수 (%s/%s)' % (__stCpStockConclusion.get_sell_count(), len(self.current_purchase_stock_list),
                        __stCpStockConclusion.get_buy_count(), len(__투자_후보_이름))
                        print(__log)
                        log.log_write(__log)

                        __timeout_count+=1
                        if __timeout_count > __timeout:
                            __bExit = True
                            break
                        if (__bBuyComplete == True) & (__bSellComplete == True):
                            __bExit = True
                            break

# >>> 모든 subscribe 해제
                    # __stCpStockConclusion.unsubscribe()
                    # 매도 종목 unsubscribe
                    # for i in range(len(self.current_purchase_stock_list)):
                    #     __code = self.stUtils.get_code_from_name(self.current_purchase_stock_list[i])
                    #     __stCpStockConclusion.unsubscribe(__code, __stCpStockConclusion)
                    # # 매수 종목 unsubscribe
                    # for i in range(len(__투자_후보_이름)):
                    #     __code = self.stUtils.get_code_from_name(__투자_후보_이름[i])
                    #     __stCpStockConclusion.unsubscribe(__code, __stCpStockConclusion)

                if __bDBG == True:
                    __bExit = True


            if __bExit == True:
                break
                

# [TEST] 장 열리기 전에 매수 걸어 놓으면 어떻게 되는지 확인
<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
    def test_algorithm(self):
        __구매_주식_1 = '큐브엔터'
        __구매_주식_2 = 'SM C&C'

        __subscribe_code_list = []
        __subscribe_code_list.append(__구매_주식_1)
        __subscribe_code_list.append(__구매_주식_2)

        __stCpStockConclusion = creon_1_SB_PB.CpPBConclusion()
        __stCpStockConclusion.subscribe(__subscribe_code_list, __stCpStockConclusion)

        print('self.stInit.is_creon_connected_as_admin()', self.stInit.is_creon_connected_as_admin())
        trade_init = self.stTrading.do_trade_init()
        if trade_init == False:
            print('trade_init fail')
            exit()
        # def 주식_주문(self, 매매, stockName, 주문단가, 주문수량, 주문호가구분코드='01', bPrint=False, bTest=False):
        주문_목록 = []
        __stockInfo = self.stStockInfo.getInfoDetail(__구매_주식_1, bPrint=True)
        __현재가 = __stockInfo[0]
        __주문코드 = self.stTrading.주식_주문(
            매매 = 1, # 1: 매도, 2: 매수
            stockName = __구매_주식_1,
=======




    def test_algorithm(self):
        __구매_주식명 = '큐브엔터'

        if self.stInit.do_creon_forced_reconnect() == False:
            exit()

        if self.stTrading.do_trade_init() == False:
            exit()

        # def 주식_주문(self, 매매, stockName, 주문단가, 주문수량, 주문호가구분코드='01', bPrint=False, bTest=False):
        __주문코드 = self.stTrading.주식_주문(
            매매 = 2, # 매수
            stockName = __구매_주식명,
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py
            주문단가 = 0,
            주문수량 = 1,
            주문호가구분코드='03',
            bPrint=True,
<<<<<<< Updated upstream:stock/creon/trading_algo/creon_99_algorithm.py
            bTest=False,
        )
        __item = {}
        __item['주식명'] = __구매_주식_1
        __item['현재가'] = __현재가
        __item['주문코드'] = __주문코드

        주문_목록.append(__item)

        __stockInfo = self.stStockInfo.getInfoDetail(__구매_주식_2, bPrint=True)
        __현재가 = __stockInfo[0]
        __주문코드 = self.stTrading.주식_주문(
            매매 = 1, # 1: 매도, 2: 매수
            stockName = __구매_주식_2,
            주문단가 = 0,
            주문수량 = 3,
            주문호가구분코드='03',
            bPrint=True,
            bTest=False,
        )

        __item = {}
        __item['주식명'] = __구매_주식_2
        __item['현재가'] = __현재가
        __item['주문코드'] = __주문코드

        주문_목록.append(__item)

        json_utils.json_write('buy_list_2020_0302.json', 'all', 주문_목록)


        while True:
            __log = 'buy count: %s, sell count: %s, conclusion: %s' % (__stCpStockConclusion.get_buy_count(), __stCpStockConclusion.get_sell_count(),  __stCpStockConclusion.get_conclusion())
            print(__log)
            log.log_write(str(__log))
            # PumpWaitingMessages()
            sleep(2)


        # __주문코드 = self.stTrading.주식_주문(
        #     매매 = 1, # 매수
        #     stockName = __구매_주식명,
        #     주문단가 = 0,
        #     주문수량 = 1,
        #     주문호가구분코드='03',
        #     bPrint=True,
        # )


if __name__ == '__main__':
    # Algorithm().algorithm_4__buy_yesterday_low_price__sell_today_high_price()

    Algorithm().test_algorithm()
=======
        )

        __주문코드 = self.stTrading.주식_주문(
            매매 = 1, # 매수
            stockName = __구매_주식명,
            주문단가 = 0,
            주문수량 = 1,
            주문호가구분코드='03',
            bPrint=True,
        )


if __name__ == '__main__':
    Algorithm().algorithm_4__buy_yesterday_low_price__sell_today_high_price()
>>>>>>> Stashed changes:stock/creon/util/creon_99_algorithm.py
