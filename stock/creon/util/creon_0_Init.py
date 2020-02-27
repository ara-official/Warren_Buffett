import win32com.client
import ctypes

import os
# from pywinauto import application # python 3.x 에서 사용 불가
import subprocess

from time import sleep

from . import login

class Connection:
    def __init__(self, logging=False):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.logging = logging

        self.log_msg = ''

    def print_log_msg(self):
        print(self.log_msg)
        self.logging = ''

    def do_creon_forced_reconnect(self): # kill_creon() 을
        self.kill_creon()
        connect = self.run_creon(login.id, login.pwd, login.pwdcert)
        __wait_time = 40
        print('forced reconnect, wait %s seconds' % (__wait_time))
        sleep(__wait_time)
        
        return connect

    def kill_creon(self):
        print('[kill_creon]')
        os.system('taskkill /IM coStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%coStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    def run_creon(self, id, pwd, pwdcert):
        print('[run_creon]')
        cmd = [
            'powershell.exe', 
            'C:\CREON\STARTER\coStarter.exe /prj:cp /id:%s /pwd:%s /pwdcert:%s /autostart' % (id, pwd, pwdcert),
            'Start-Process', 
            ]
        subprocess.run(cmd, shell=True)
        
        while True:
            if self.is_creon_connected_as_admin() == True:
                break
            print(self.print_log_msg())
            sleep(2)
        return True

    def is_creon_connected_as_admin(self):
        connect = False
        admin = self.is_vs_run_as_admin() # 관리자 권한 실행 확인

        if admin == False:
            connect = False
        else:
            connect = self.is_creon_connected()

        return connect

    def is_vs_run_as_admin(self): # vs: visual studio
        value = ctypes.windll.shell32.IsUserAnAdmin()
        if value == False:
            self.log_msg += '[오류 No!]: 관리자 권한으로 실행하세요 | '
        else:
            self.log_msg += '[정상 Yes]: 관리자 권한으로 실행된 프로세스 | '
        
        return value
        
    def is_creon_connected(self):
        ret = False

        connect = self.instCpCybos.IsConnect

        if connect == 0:
            self.log_msg += '연결끊김 | '
        elif connect == 1:
            self.log_msg += '연결정상 | '

        connect_server = self.instCpCybos.ServerType # 0: 연결끊김, 1: cybosplus 서버, 2: HTS 보통서버

        if connect_server == 0:
            self.log_msg += '서버연결 끊김 | '
        else:
            self.log_msg += '서버연결 되어있음 (%s) | ' % (connect_server)

        if (connect == 1) & (connect_server != 0):
            ret = True
        
        return ret
