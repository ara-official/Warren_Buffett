import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.abspath(os.path.dirname(__file__)))

from stock.creon.trading_algo import creon_99_algorithm

from stock.creon.util import utils


# for test
from stock.creon.util import creon_0_Init
from stock.creon.util import creon
from stock.creon.util import login

from time import sleep

if __name__ == '__main__':
    print('111111111111111111111111111111111111111111111111111111111111111111')
    print('111111111111111111111111111111111111111111111111111111111111111111')
    print('111111111111111111111111111111111111111111111111111111111111111111')
    # os.system('python C:\\Users\\SMS\\Desktop\\PROGRAMMING\\Warren_Buffett\\stock\\creon\\util\\creon_99_algorithm.py')

    __cnt = 0
    while True:
        __cnt+=1
        creon_99_algorithm.Algorithm().algorithm_4__buy_yesterday_low_price__sell_today_high_price()

        if __cnt >= 5:
            break
    exit()

    stInit = creon_0_Init.Connection()
    stInit.kill_creon()
    stInit.run_creon(login.id, login.pwd, login.pwdcert)
    stTrading = creon.Trading()
    stTrading.do_trade_init()
    __주문코드 = stTrading.주식_주문(
        매매 = 2, # 매수
        stockName = '삼성전자',
        주문단가 = 0,
        주문수량 = 1,
        주문호가구분코드='03',
        bPrint=True,
    )

    sleep(5)
    stInit.kill_creon()
    stInit.run_creon(login.id, login.pwd, login.pwdcert)
    __주문코드 = stTrading.주식_주문(
        매매 = 2, # 매수
        stockName = '삼성전자',
        주문단가 = 0,
        주문수량 = 1,
        주문호가구분코드='03',
        bPrint=True,
    )
    exit()

    stAlgorithm = creon_99_algorithm.Algorithm()
    stAlgorithm.algorithm_4__buy_yesterday_low_price__sell_today_high_price()
    exit()

    item = {} # dictionary
    item['원주문번호'] = 1
    item['종목명'] = '삼숭'
    item['주문수'] = 10
    print(item)
    item_list = []
    item_list.append(item)
    item_list.append(item)
    item_list.append(item)
    
    print(item_list)