import os
import sys
from datetime import datetime
from stock.creon.util import utils 

def log_write(content):
    reletive_path=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    json_file_name=str(reletive_path)+'\\trade_log\\'+datetime.today().strftime("%Y%m%d")+'.LOG'
    
    # print(json_file_name)
    __cur_time = utils.Utils().현재_시간()
    temp=str(__cur_time).split('.')
    
    content = str(content)
    content = '['+temp[0]+'] '+content+'\n'
    f = open(json_file_name, 'a+', encoding='utf-8')
    f.write(content)
    f.close()
    
