import os
import sys

dir = os.getcwd()
dir_split = dir.split('\\')
cur_dir_depth = 2 # TODO: (minsik.son) 이 값도 자동으로 넣도록 수정 필요함.
len = len(dir_split) - cur_dir_depth
root_dir = "\\".join(dir_split[0:len])
# print(dir_split)
# print(root_dir)
sys.path.append(root_dir)

from web_crawling.webcrawler import crawler

import web_crawling.login as login

class Crawling_Stock_Info:
    def __init__(self):
        self.websiteCrawler = crawler.WebsiteCrawler(skip_screen=False)

    def get_crwaler(self):
        return self.websiteCrawler

    def get_driver(self):
        driver = self.websiteCrawler.get_driver()

    def loging_investing(self):
        # [1] investing.com 이동
        self.websiteCrawler.move_to_url("https://kr.investing.com/")

        login_xpath='//*[@id="userAccount"]/div/a[1]'
        bResult = self.websiteCrawler.click_by_xpath(login_xpath)
        
        self.websiteCrawler.sleep(20)
        id_path='input[id="loginFormUser_email"]'
        pwd_path='input[id="loginForm_password"]'
        btn_xpath='//*[@id="signup"]/a'
        
        # [2] 로그인
        __u_input = self.websiteCrawler.get_browser().find_one(id_path)
        __u_input.send_keys(login.id)
        __u_input = self.websiteCrawler.get_browser().find_one(pwd_path)
        __u_input.send_keys(login.pwd)
        __u_input = self.websiteCrawler.get_browser().find_one_by_xpath(btn_xpath)
        __u_input.click()

        print(login.id)
        print(login.pwd)
        
    def get_CURRENT_ASSET(self, stock_name, stock_code):
        delay_time = 3 # 초
        # xpath
        구글_첫_번째_검색결과_xpath='//*[@id="rso"]/div[1]/div/div[1]/a/h3' # 광고인 경우 존재
        구글_두_번째_검색결과_xpath='//*[@id="rso"]/div[2]/div/div[1]/a/h3'

        유동자산_xpath = '//*[@id="parentTr"]/td[2]'
        셋째_탭_xpath = '//*[@id="pairSublinksLevel1"]/li[3]/a'
        넷째_탭_xpath = '//*[@id="pairSublinksLevel1"]/li[4]/a'
        하위_셋째_탭_xpath = '//*[@id="pairSublinksLevel2"]/li[3]/a'

        bRetry = False

        # self.websiteCrawler.move_to_url("https://kr.investing.com/equities/samsung-electronics-co-ltd")
        # self.websiteCrawler.move_to_url("https://kr.investing.com/")
        self.websiteCrawler.move_to_url("https://www.google.com/")
        # 검색어 = 'kr.investing.com 대차대조표 '
        # 검색어 = '검색 investing.com'
        검색어 = 'kr.investing.com 재정 상황 대차 대조표'
        
        # 검색어 += ' %s 실적' % (stock_name)
        검색어 += ' %s' % (stock_name)
        검색어 += ' (%s)' % (stock_code)
        print('검색어: %s' % (검색어))
        
        self.websiteCrawler.sleep(3)
        self.websiteCrawler.input_and_click_btn(검색어, crawler.WebsiteCrawler.XPATH_GOOGLE_INPUT, bPrint=False)

        bResult = self.websiteCrawler.click_by_xpath(구글_첫_번째_검색결과_xpath)
        # bResult = self.websiteCrawler.click_by_xpath(구글_두_번째_검색결과_xpath)
        if bResult == False:
            print('2222222222222222222222222222222')
            return 0
        else:
            print('2222222222222222222222222222222 - 2')

        bRetry = True
        self.websiteCrawler.sleep(5)
        # [1] 바로 유동자산값에 접근
        # print('유동자산_xpath')
        # 유동자산 = self.websiteCrawler.get_data_by_xpath(유동자산_xpath)
        # if 유동자산 == None:
        #     print('1111111111111111111111111111111 - 1')

        #     bRetry = True
        # else:
        #     유동자산 = float(유동자산) * 1000000
        #     print('유동자산:%s' % (유동자산))
        #     print('1111111111111111111111111111111 - 2')
        #     return 유동자산

        self.websiteCrawler.sleep(delay_time)
        if bRetry == True:
            print('하위_셋째_탭_xpath')
            bResult = self.websiteCrawler.click_by_xpath(하위_셋째_탭_xpath)
            if bResult == False:
                print('343434343434343434343434343434 - 1')
                bRetry = True
            else:
                self.websiteCrawler.sleep(delay_time)
                print('유동자산_xpath')
                유동자산 = self.websiteCrawler.get_data_by_xpath(유동자산_xpath)
                if 유동자산 == None:
                    print('343434343434343434343434343434 - 2')
                    bRetry = True
                else:
                    print('343434343434343434343434343434 - 3')

                    유동자산 = float(유동자산) * 1000000
                    print('유동자산:%s' % (유동자산))
                    return 유동자산

        self.websiteCrawler.sleep(delay_time)
        if bRetry == True:
            print('셋째_탭_xpath')
            bResult = self.websiteCrawler.click_by_xpath(셋째_탭_xpath)
            if bResult == True:
                self.websiteCrawler.sleep(delay_time)
                print('하위_셋째_탭_xpath')
                bResult = self.websiteCrawler.click_by_xpath(하위_셋째_탭_xpath)
                if bResult == False:
                    bRetry = True
                else:
                    bRetry = False
            else:
                bRetry = True

        self.websiteCrawler.sleep(delay_time)
        if bRetry == True:
            print('444444444444444444444444444 - 1')
            bResult = self.websiteCrawler.click_by_xpath(넷째_탭_xpath)
            if bResult == True:
                self.websiteCrawler.sleep(delay_time)
                print('하위_셋째_탭_xpath')
                bResult = self.websiteCrawler.click_by_xpath(하위_셋째_탭_xpath)
            else:
                print('444444444444444444444444444 - 2')
                return 0

        self.websiteCrawler.sleep(delay_time)
        print('유동자산_xpath')
        유동자산 = self.websiteCrawler.get_data_by_xpath(유동자산_xpath)
        if 유동자산 == None:
            print('55555555555555555555555555')
            return 0
        유동자산 = float(유동자산) * 1000000
        print('유동자산:%s' % (유동자산))

        print('66666666666666666666666')
        return 유동자산
