import sys
import argparse
from datetime import datetime

from stock.quantity import utils as quant_util
from stock.creon.util import creon_0_Init, creon_98_stocks_by_industry
from stock.creon.util import utils as creon_util

from data_process import file_inout

def usage():
    how_to_use = ''' 현재는 NCAV 기반으로 종목을 추천합니다.
        example)
        python main_quant.py -sn 삼성전자
        python main_quant.py -a
        python main_quant.py -a -d
        python main_quant.py -a --debug
        python main_quant.py -a -p 2
        python main_quant.py -s -sn 삼성전자 -bd 20190622 -sd 20200622

        용어)
        PBR : Price to Book Ratio (= 현재가 / BPS)
        BPS : Book Per Share
        PER : Price to Earning Ratio
    '''
    return how_to_use

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="퀀트 투자 ver 1.0", usage=usage())
    parser.add_argument("-a", "--all_stock", action="store_true", help="KOSPI & KOSDAQ")
    parser.add_argument("-sn", "--stock_name", default="")
    parser.add_argument("-s", "--sim", action="store_true")
    parser.add_argument("-bd", "--buy_date", default="")
    parser.add_argument("-sd", "--sell_date", default="")
    parser.add_argument("-p", "--per", default=0, type=float)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-id", "--id")
    parser.add_argument("-pwd", "--password")
    parser.add_argument("-cp", "--certpassword")
    parser.add_argument("-w", "--weight", default=1.5, type=float)

    args = parser.parse_args()

    DEBUG = args.debug

    # args.weight = 1 # for TEST


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
    

    # quant
    if args.sim == True:
        # sn 필요
        if args.stock_name == "":
            print(usage())
            exit()
        # bd, sd 필요
        if args.buy_date == "":
            print(usage())
            exit()
        if args.sell_date == "":
            print(usage())
            exit()
        
        buy_date = datetime.strptime(args.buy_date, "%Y%m%d")
        sell_date = datetime.strptime(args.sell_date, "%Y%m%d")

        q_buy = quant_util.Quant_Utils(year=buy_date.year, bPrint=DEBUG)
        q_sell = quant_util.Quant_Utils(year=sell_date.year, bPrint=DEBUG)

        # q_buy.get_NCAV_by_date(args.stock_name, buy_date, bPrint=DEBUG)
        q_buy.get_NCAV_by_date(args.stock_name, args.buy_date, weight=args.weight, bPrint=DEBUG)
        q_sell.get_NCAV_by_date(args.stock_name, args.sell_date, weight=args.weight, bPrint=DEBUG)


    elif args.all_stock == True:
        q = None
        if args.buy_date != "":
            buy_date = datetime.strptime(args.buy_date, "%Y%m%d")
            # sell_date = datetime.strptime(args.sell_date, "%Y%m%d")
            q = quant_util.Quant_Utils(buy_date.year)
        else:
            q = quant_util.Quant_Utils(bPrint=DEBUG)

        __marketType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피']
        stock_list = creon_98_stocks_by_industry.StocksByIndustry().getStockListByMarket(__marketType)
        __marketType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스닥']
        stock_list += creon_98_stocks_by_industry.StocksByIndustry().getStockListByMarket(__marketType)

        date = datetime.today().strftime("%Y%m%d%H%M")
        if args.buy_date != "":
            date = args.buy_date
        output_file_name = date + "_NCAV.txt"
        
        path='./output/%s' % (output_file_name)
        file_inout.write_to_file(path=path, data="", option='w')

        if DEBUG == True:
            print(path)

        count = 0
        stock_name = ''
        stock_code = ''
        sleep_count = 0
        bListIsCode = True
        for i in stock_list:
            count += 1

            if count < 40: # <- 이 번호? 부터 crawling
                continue

            if bListIsCode == True:
                stock_name = creon_util.Utils().get_name_from_code(i)
                stock_code = i
            else:
                stock_name = i
                stock_code = creon_util.Utils().get_code_from_name(i)

            print_1 = '[%s] %s (%s)' % (count, stock_name, stock_code)

            구매여부 = ""
            print_2 = ""
            if args.buy_date != "":
                구매여부, print_2 = q.get_NCAV_by_date(stock_name, args.buy_date, weight=args.weight)
            else:
                구매여부, print_2 = q.NCAV(stock_name, weight=args.weight, bCrawling=False)
                PER = q.get_PER(stock_name)
                print_1 += " (PER: %s)" % (round(PER, 5))
                if args.per > 0:
                    if PER > args.per:
                        구매여부 = False
                    if PER == 0:
                        구매여부 = False
            print_5 = '==========================================================================================='

            print(print_1)
            print(print_2)
            print(print_5)

            if 구매여부 == False:
                continue
            
            print_4 = ""
            if args.buy_date == "":
                PBR, 현재가, BPS = q.get_PBR(stock_name)
                print_4 = "PBR: %s, 현재가: %s, BPS: %s" % (round(PBR, 5), round(현재가), round(BPS))

                print_1 += " ("
                print_1 += print_4
                print_1 += ")" 

            file_inout.write_to_file(path=path, data=print_1, option='a')
            file_inout.write_to_file(path=path, data=print_2, option='a')
            file_inout.write_to_file(path=path, data=print_5, option='a')
    elif args.stock_name != "":
        q = quant_util.Quant_Utils(bPrint=DEBUG)

        구매여부, print_2 = q.NCAV(args.stock_name, weight=args.weight, bCrawling=False)

        print_1 = '이름: %s, 구매여부: %s' % (args.stock_name, 구매여부)
        PER = q.get_PER(args.stock_name)
        print_1 += " (PER: %s)" % (round(PER, 5))

        PBR, 현재가, BPS = q.get_PBR(args.stock_name)
        print_4 = "PBR: %s, 현재가: %s, BPS: %s" % (round(PBR, 5), format(round(현재가), ','), format(round(BPS), ','))
        print_5 = '==========================================================================================='
        
        print(print_5)
        print(print_1)
        print(print_2)
        print(print_4)
        print(print_5)
    else:
        print(parser.print_help())
