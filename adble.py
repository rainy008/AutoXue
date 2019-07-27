#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: quizXue
@file: adble.py
@author: kessil
@contact: https://github.com/kessil/quizXue/
@time: 2019年07月26日 11:14:13
@desc: Life is short, you need Python
'''
from time import sleep
import subprocess
from configparser import ConfigParser

class Adble(object):
    def __init__(self, device='mumu'):
        cfg = ConfigParser()
        cfg.read('./config.ini')
        self.filename = cfg.get(device, 'xml_uri')
        
        if 'mumu' == device:
            self.connect_mumu()

    def connect_mumu(self):
        '''连接MuMu模拟器
            windows: adb shell connect 127.0.0.1:7555
            MacOS: adb shell connect 127.0.0.1:5555
        '''
        print("默认连接Windows平台MuMu模拟器(测试时版本号:v2.2.7)")
        subprocess.check_call('adb connect 127.0.0.1:7555', shell=True, stdout=subprocess.PIPE)
    
    def get_xml(self):
        subprocess.check_call(f'adb shell uiautomator dump /sdcard/ui.xml', shell=True, stdout=subprocess.PIPE)
        sleep(1)
        subprocess.check_call(f'adb pull /sdcard/ui.xml {self.filename}', shell=True, stdout=subprocess.PIPE)

    def swipe(self, sx, sy, dx, dy, duration):
        ''' swipe from (sx, xy) to (dx, dy) in duration ms'''
        subprocess.check_call(f'adb shell input swipe {sx} {sy} {dx} {dy} {duration}', shell=True, stdout=subprocess.PIPE)

    def tap(self, x, y):
        # subprocess.check_call(f'adb shell input tap {x} {y}', shell=True, stdout=subprocess.PIPE)
        '''改进tap为长按50ms，避免单击失灵'''
        self.swipe(x, y, x, y, 50)

if __name__ == "__main__":
    adble = Adble()
    adble.get_xml()