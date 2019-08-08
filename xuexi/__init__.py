#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: StudyEveryday
@file: __init__.py
@author: kessil
@contact: https://github.com/kessil/StudyEveryday/
@time: 2019-08-02(星期五) 16:35
@Copyright © 2019. All rights reserved.
'''

from pathlib import Path
import re
from configparser import ConfigParser
from .logs import create_logger


path = Path(__file__).parent
for item in ['json', 'xml', 'xls']:
    p = path/'src'/item
    p.mkdir(parents=True, exist_ok=True)
logger = create_logger('xuexi', 'DEBUG')
cfg = ConfigParser()
cfg.read(path/'config-default.ini', encoding='utf-8')
cfg.read(path/'config-custom.ini', encoding='utf-8')

class App(object):
    def __init__(self):
        self.rules = cfg.get('common', 'device')
        self.xmluri = Path(cfg.get(self.rules, 'xml_uri'))
        self.ad = adble.Adble(
                            self.xmluri,
                            cfg.getboolean(self.rules, 'is_virtual_machine'), 
                            cfg.get(self.rules, 'host'),
                            cfg.getint(self.rules, 'port'))
        self.xm = xmler.Xmler(self.xmluri)

    def _art_run(self):
        logger.info(f'阅读文章功能正在实现中')

    def _vdo_run(self):
        logger.info(f'视听学习功能正在实现中')

    def _quiz_run(self, day, chg):
        logger.debug(f'我要答题，开始')
        qApp = Quiz(self.rules, self.ad, self.xm)
        qApp.start(day, chg)

    def start(self, art, vdo, day, chg):
        if art:
            self._art_run()
        if vdo:
            self._vdo_run()
        if day or chg:
            with timer.Timer() as t:
                self._quiz_run(day, chg)
            logger.info(f'答题耗时 {t.elapsed} 秒')


    def __del__(self):
        self.ad.close()


    
        

from .quiz import Quiz
from .common import adble, xmler, timer
from .model import Model