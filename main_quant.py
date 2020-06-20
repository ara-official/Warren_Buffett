import argparse
from datetime import datetime

from stock.quantity import utils as quant_util
from stock.creon.util import creon_0_Init, creon_98_stocks_by_industry
from stock.creon.util import utils as creon_util


DEBUG = False

def usage():
    how_to_use = ''' 현재는 NCAV 기반으로 종목을 추천합니다.
        example)
        python main_quant.py -u 삼성전자
        python main_quant.py -a
    '''
    return how_to_use

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="퀀트 투자 ver 1.0", usage=usage())
    parser.add_argument("-u", "--stock_name", help="insta id")
    parser.add_argument("-a", "--all_stock", action="store_true", help="KOSPI & KOSDAQ")
    parser.add_argument("-id", "--id")
    parser.add_argument("-pwd", "--password")
    parser.add_argument("-cp", "--certpassword")
    args = parser.parse_args()
    if DEBUG == True:
        print("args : %s" % (args))

    # exception case
    if (args.stock_name == None) & (args.all_stock == False):
        print(usage())
        exit()
        
    # login
    if creon_0_Init.Connection(logging=DEBUG).is_creon_connected() == False:
        creon_0_Init.Connection(logging=DEBUG).do_creon_forced_reconnect(args.id, args.password, args.certpassword)
    else:
        if DEBUG == True:
            print('[CREON] already connected~')
    
    q = quant_util.Quant_Utils(bPrint=DEBUG)

    # quant
    if args.all_stock == True:
        __marketType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피']
        stock_list = creon_98_stocks_by_industry.StocksByIndustry().getStockListByMarket(__marketType)
        __marketType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스닥']
        stock_list += creon_98_stocks_by_industry.StocksByIndustry().getStockListByMarket(__marketType)



        # date = datetime.today().strftime("%Y%m%d%H%M%S")
        date = datetime.today().strftime("%Y%m%d%H%M")
        output_file_name = date + "_NCAV.txt"
        
        path='./output/%s' % (output_file_name)
        if DEBUG == True:
            print(path)

        count = 0
        stock_name = ''
        stock_code = ''
        sleep_count = 0
        bListIsCode = True
        for i in stock_list:
            count += 1
            # if count < 382: # <- 이 번호? 부터 crawling
            #     continue

            if bListIsCode == True:
                stock_name = creon_util.Utils().get_name_from_code(i)
                stock_code = i
            else:
                stock_name = i
                stock_code = creon_util.Utils().get_code_from_name(i)

            print_1 = '[%s] 이름: %s, 코드: %s' % (count, stock_name, stock_code)

            구매여부, print_2 = q.NCAV(stock_name, bCrawling=False)
            # print_2 = '구매여부: %s' % (구매여부)

            print(print_1)
            print(print_2)
            print(print_3)
            print_5 = '=============================================================='
            print(print_5)

            if 구매여부 == False:
                continue
            
            PBR, 현재가, BPS = q.get_PBR(args.stock_name)
            print_4 = "PBR: %s, 현재가: %s, BPS: %s" % (PBR, 현재가, BPS)

            file_inout.write_to_file(path=path, data=print_1, option='a')
            file_inout.write_to_file(path=path, data=print_2, option='a')
            file_inout.write_to_file(path=path, data=print_3, option='a')
            file_inout.write_to_file(path=path, data=print_4, option='a')
            file_inout.write_to_file(path=path, data=print_5, option='a')
    else:
        구매여부, print_2 = q.NCAV(args.stock_name, bCrawling=False)
        # print_2 = '구매여부: %s' % (구매여부)

        print_1 = '이름: %s, 구매여부: %s' % (args.stock_name, 구매여부)

        PBR, 현재가, BPS = q.get_PBR(args.stock_name)
        print_4 = "PBR: %s, 현재가: %s, BPS: %s" % (PBR, 현재가, BPS)
        print_5 = '=============================================================='
        
        print(print_5)
        print(print_1)
        print(print_2)
        print(print_4)
        print(print_5)