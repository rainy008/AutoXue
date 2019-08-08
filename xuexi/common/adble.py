#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: StudyEveryday
@file: common.py
@author: kessil
@contact: https://github.com/kessil/StudyEveryday/
@time: 2019-07-30(星期二) 20:31
@Copyright © 2019. All rights reserved.
'''
import re
import subprocess
from time import sleep
from pathlib import Path
from .. import logger


class Adble(object):
    def __init__(self, path=Path('./ui.xml'), is_virtual:bool=True, host='127.0.0.1', port=7555):
        # subprocess.Popen(f'adb version', shell=True)
        self.path = path
        self.is_virtual = is_virtual
        self.host = host
        self.port = port
        if self.is_virtual:
            self._connect()            
        else:            
            logger.info(f'请确保安卓手机连接手机并打开USB调试!')
        self.ime = self._getIME()
        self._setIME('com.android.adbkeyboard/.AdbIME')

    def _connect(self):
        '''连接模拟器adb connect host:port'''
        logger.debug(f'正在连接模拟器{self.host}:{self.port}')
        if 0 == subprocess.check_call(f'adb connect {self.host}:{self.port}', shell=True, stdout=subprocess.PIPE):
            logger.info(f'连接模拟器{self.host}:{self.port} 成功')
        else:
            logger.info(f'断开模拟器{self.host}:{self.port} 失败')
        
    def _disconnect(self):
        '''连接模拟器adb connect host:port'''
        logger.debug(f'正在断开模拟器{self.host}:{self.port}')
        if 0 == subprocess.check_call(f'adb disconnect {self.host}:{self.port}', shell=True, stdout=subprocess.PIPE):
            logger.info(f'断开模拟器{self.host}:{self.port} 成功')
        else:
            logger.info(f'断开模拟器{self.host}:{self.port} 失败')

    def wm_size(self):
        res = subprocess.check_output('adb shell wm size', shell=False)
        if isinstance(res, bytes):
            wmsize = re.findall(r'\d+', str(res, 'utf-8'))
        else:
            wmsize = re.findall(r'\d+', res)
        logger.debug(f'屏幕分辨率：{wmsize}')
        res = [int(x) for x in wmsize]
        return res
    

    def _setIME(self, ime):
        logger.debug(f'设置输入法 {ime}')
        logger.debug(f'正在设置输入法 {ime}')
        if 0 == subprocess.check_call(f'adb shell ime set {ime}', shell=True, stdout=subprocess.PIPE):
            logger.debug(f'设置输入法 {ime} 成功')
        else:
            logger.debug(f'设置输入法 {ime} 失败')

    def _getIME(self)->list:
        logger.debug(f'获取系统输入法list')
        res = subprocess.check_output(f'adb shell ime list -s', shell=False)
        if isinstance(res, bytes):
            # ime = re.findall(r'\d+', str(res, 'utf-8'))
            ime = re.findall(r'\S+', str(res, 'utf-8'))
        else:
            ime = re.findall('\S+', res)
        logger.debug(f'系统输入法：{ime}')
        return ime[0]
        

    def uiautomator(self, path=None, filesize=9000):
        if not path:
            path = self.path
        for i in range(3):
            if path.exists():
                path.unlink()
            else:
                logger.debug('文件不存在')
            subprocess.check_call(f'adb shell uiautomator dump /sdcard/ui.xml', shell=True, stdout=subprocess.PIPE)
            # sleep(1)
            subprocess.check_call(f'adb pull /sdcard/ui.xml {path}', shell=True, stdout=subprocess.PIPE)
            if filesize < path.stat().st_size:
                break

    def screenshot(self, path=None):
        if not path:
            path = self.path
        subprocess.check_call(f'adb shell screencap -p /sdcard/ui.png', shell=True, stdout=subprocess.PIPE)
        # sleep(1)
        subprocess.check_call(f'adb pull /sdcard/ui.png {path}', shell=True, stdout=subprocess.PIPE)

    def swipe(self, sx, sy, dx, dy, duration):
        ''' swipe from (sx, xy) to (dx, dy) in duration ms'''
        # adb shell input swipe 500 500 500 200 500
        logger.debug(f'滑动操作 ({sx}, {sy}) --{duration}ms-> ({dx}, {dy})')
        res = subprocess.check_call(f'adb shell input swipe {sx} {sy} {dx} {dy} {duration}', shell=True, stdout=subprocess.PIPE)
        # sleep(1)
        return res

    def tap(self, x, y=None):
        # subprocess.check_call(f'adb shell input tap {x} {y}', shell=True, stdout=subprocess.PIPE)
        '''改进tap为长按50ms，避免单击失灵'''
        if y is not None:
            if isinstance(x, int) and isinstance(y, int):
                dx, dy = int(x), int(y)
            else:
                logger.debug(f'输入坐标有误')
        else:
            dx, dy = int(x.real), int(x.imag)
        logger.debug(f'触摸操作 ({dx}, {dy})')
        return self.swipe(dx, dy, dx, dy, 50)

    def back(self):
        # adb shell input keyevent 4 
        logger.debug(f'adb 触发<返回按钮>事件')
        subprocess.check_call(f'adb shell input keyevent 4', shell=True, stdout=subprocess.PIPE)


    def text(self, msg):
        logger.debug(f'输入文本 {msg}')
        # subprocess.check_call(f'adb shell input text {msg}', shell=True, stdout=subprocess.PIPE)
        subprocess.check_call(f'adb shell am broadcast -a ADB_INPUT_TEXT --es msg {msg}', shell=True, stdout=subprocess.PIPE)

    def close(self):
        self._setIME(self.ime)
        if self.is_virtual:
            self._disconnect()

if __name__ == "__main__":
    from argparse import ArgumentParser
    from .. import logger
    logger.debug('running adble.py')
    parse = ArgumentParser()
    parse.add_argument(dest='filename', metavar='filename', nargs="?", type=str, help='目标文件路径')
    parse.add_argument('-s', '--screenshot', metavar='screenshot', nargs='?', const=True, type=bool, default=False, help='截图并上传')
    parse.add_argument('-t', '--text', metavar='text', type=str, default='不忘初心牢记使命', help='输入文字')
    parse.add_argument('-u', '--uiautomator', metavar='uiautomator', nargs='?', const=True, type=bool, default=False, help='解析布局xml并上传')
    parse.add_argument('-v', '--virtual', metavar='virtual', nargs='?', const=True, type=bool, default=False, help='是否模拟器')
    args = parse.parse_args()
    adb = Adble(f'noname', args.virtual)
    if args.filename:
        path = Path(args.filename)
        if args.screenshot:
            adb.screenshot(path.with_suffix('.png'))
            print(f'截图保存成功')
        if args.uiautomator:
            # sleep(2)
            adb.uiautomator(path.with_suffix('.xml'))
            print(f'布局保存成功')
    else:
        adb.text(args.text)
        print(f'输入文字{args.text}')

    adb.close()

    
