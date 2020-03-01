import win32com.client
import ctypes

import os
# from pywinauto import application # python 3.x 에서 사용 불가
import subprocess

from time import sleep

from util import login

class Connection:
    def __init__(self, logging=False):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.logging = logging

        self.log_msg = ''

    def print_log_msg(self):
        print(self.log_msg)
        self.log_msg = ''

    def do_creon_forced_reconnect(self):
        print('[do_creon_forced_reconnect]')
        self.kill_creon()
        connect = self.run_creon(login.id, login.pwd, login.pwdcert)
        
        return connect

    def kill_creon(self):
        # IM: IMage name
        print('[kill_creon] 1')
        # os.system('taskkill /IM coStarter* /F /T')
        # os.system('taskkill /IM CpStart* /F /T')
        # os.system('taskkill /IM DibServer* /F /T')

        #NOTE: /F /T 를 붙일 경우, CpStart.exe 가 종료되지 않는 경우 존재.
        # os.system('taskkill /IM coStarter*')
        # os.system('taskkill /IM CpStart*')
        # os.system('taskkill /IM DibServer*')

        r = subprocess.Popen('taskkill /IM coStarter*', shell=True).wait()
        if r == 1:
            print('running error: %s' % (r))
        r = subprocess.Popen('taskkill /IM CpStart* /F', shell=True).wait()
        if r == 1:
            print('running error: %s' % (r))
        r = subprocess.Popen('taskkill /IM DibServer*', shell=True).wait()
        if r == 1:
            print('running error: %s' % (r))
        
        os.system('wmic process where "name like \'%coStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

        print('[kill_creon] 2')
        
        __cnt = 0
        while self.is_creon_connected_as_admin() == True:
            __cnt+=1
            print(self.is_creon_connected_as_admin(), __cnt)

            r = subprocess.Popen('taskkill /IM python*', shell=True).wait()
            if r == 1:
                print('running error: %s' % (r))

            os.system('wmic process where "name like \'%python%\'" call terminate')

            self.print_log_msg()
            if self.is_creon_connected_as_admin() == False:
                break

        self.print_log_msg()
  
        return True

    def run_creon(self, id, pwd, pwdcert):
        ret = True
        print('[run_creon]')

        cmd = [
            'powershell.exe', 
            'C:\\CREON\\STARTER\\coStarter.exe /prj:cp /id:%s /pwd:%s /pwdcert:%s /autostart' % (id, pwd, pwdcert),
            'Start-Process', 
            ]
        r = subprocess.Popen(cmd, shell=True).wait()
        if r == 1:
            print('running error: %s' % (r))
        
        if self.is_creon_connected_as_admin() == False:
            print('1111111111111111111')
            while True:
                self.print_log_msg()
                if self.is_creon_connected_as_admin() == True:
                    break
                sleep(2)
            self.print_log_msg()
        else:
            
            print('2222222222222222222')
            print('[error] 크레온에 연결이 되어 있는 상태에서 재접속 하였습니다 (종료)')
            # exit()
            ret = False
        return ret

    def is_creon_connected_as_admin(self):
        connect = False

        if self.is_vs_run_as_admin() == False: # 관리자 권한 실행 확인
            connect = False
        else:
            connect = self.is_creon_connected()

        return connect

    def is_vs_run_as_admin(self): # vs: visual studio
        value = ctypes.windll.shell32.IsUserAnAdmin()
        if value == False:
            self.log_msg += '[관리자 권한 (x)] '
        else:
            self.log_msg += '[관리자 권한 (o)] '
        
        return value
        
    def is_creon_connected(self):
        ret = False

        # connect = self.instCpCybos.IsConnect
        connect = win32com.client.Dispatch("CpUtil.CpCybos").IsConnect

        if connect == 0:
            self.log_msg += '[%s 연결 끊김 (x)] ' % (connect)
        elif connect == 1:
            self.log_msg += '[%s 연결 정상 (o)] ' % (connect)

        connect_server = win32com.client.Dispatch("CpUtil.CpCybos").ServerType # 0: 연결끊김, 1: cybosplus 서버, 2: HTS 보통서버

        if connect_server == 0:
            self.log_msg += '[%s 서버 끊김 (x)] ' % (connect_server)
        else:
            self.log_msg += '[%s 서버 연결 (o)] ' % (connect_server)

        if (connect == 1) & (connect_server != 0):
            ret = True

        self.log_msg += '[ret %s] ' % (ret)

        return ret
