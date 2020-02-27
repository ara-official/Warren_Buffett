from stock.creon.util import creon_99_algorithm

from stock.creon.util import utils

if __name__ == '__main__':

    # creon_99_algorithm.Algorithm().algorithm_3__stock_purchase_recommandation(전체기간=20, marketType=1, top=1, bPrint=True)
    creon_99_algorithm.Algorithm().algorithm_4()
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