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

import os
import re
from configparser import ConfigParser
from .logs import create_logger


basedir = os.path.abspath(os.path.dirname(__file__))
logger = create_logger('xuexi', 'DEBUG')

cfg = ConfigParser()
cfg.read(os.path.join(basedir, 'config-default.ini'), encoding='utf-8')
cfg.read(os.path.join(basedir, 'config-custom.ini'), encoding='utf-8')
# db = Model(cfg.get('common', 'database_uri'))

class App(object):
    def __init__(self):
        self.rules = cfg.get('common', 'device')
        self.xmluri = cfg.get(self.rules, 'xml_uri')
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
        logger.info(f'我要答题，开始')
        qApp = Quiz(self.rules, self.ad, self.xm)
        qApp.start(day, chg)

    def start(self, art, vdo, day, chg):
        if art:
            self._art_run()
        if vdo:
            self._vdo_run()
        if day or chg:
            self._quiz_run(day, chg)


    def __del__(self):
        self.ad.close()


    
        

from .quiz import Quiz
from .common import adble, xmler
from .model import Model