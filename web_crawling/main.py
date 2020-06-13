# investing site 의 stock_name 으로 접근
# url 뒤에 -balance-sheet 붙인 뒤 이동
# 유동자산 값 긁어옴
import os
import sys

dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 1 # TODO: (minsik.son) 이 값도 자동으로 넣도록 수정 필요함.
len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:len])
print(dir_split)
print(root_dir)
sys.path.append(root_dir)

from web_crawling import crawling_stock
from stock.creon.util import utils

if __name__ == '__main__':
    stCrawlingStockInfo = crawling_stock.Crawling_Stock_Info()
    stCrawlingStockInfo.test()

    print(utils.Utils().get_code_from_name('삼성전자'))