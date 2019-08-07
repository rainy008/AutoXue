#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: StudyEveryday
@file: __init__.py
@author: kessil
@contact: https://github.com/kessil/StudyEveryday/
@time: 2019-08-04(星期天) 19:27
@Copyright © 2019. All rights reserved.
'''
import os
import re
import json
from time import sleep
from ..common import adble, xmler
from .. import logger, cfg
from .challenge import ChallengeQuiz
from .daily import DailyQuiz

class Quiz(object):
    def __init__(self, rules, ad, xm):
        self.rules = rules
        self.ad = ad
        self.xm = xm

    def _fresh(self):
        self.ad.uiautomator()
        self.xm.load()

    def _run_daily(self):

        dq = DailyQuiz(self.rules, self.ad, self.xm)
        round = cfg.getint('common', 'daily_round')
        count = cfg.getint('common', 'daily_count')
        dq.run(round, count)
        logger.info('完成每日答题，请稍后片刻...')
        sleep(5)

    def _run_challenge(self):

        cq = ChallengeQuiz(self.rules, self.ad, self.xm)
        count = cfg.getint('common', 'challenge_count')
        cq.run(count)
        logger.info('完成挑战答题，请稍后片刻...')
        sleep(5)

    def start(self, day, chg):
        # 刷新一下
        height, width = self.ad.wm_size() # example: [1024, 576]
        x0 = width//2
        y0 = height//3
        self.ad.swipe(x0, y0, x0, y0+200, 1000)
        sleep(3)

        # 点击我的
        self._fresh()
        pos = self.xm.pos(cfg.get(self.rules, 'rule_bottom_mine'))
        self.ad.tap(pos)
        sleep(1)

        # 点击我要答题
        self._fresh()
        pos = self.xm.pos(cfg.get(self.rules, 'rule_quiz_entry'))
        self.ad.tap(pos)
        sleep(10)
        if day:
            logger.debug(f'开始每日答题')
            self._run_daily()
        else:
            logger.info(f'未选择执行每日答题')
        sleep(10)
        if chg:
            logger.debug(f'开始挑战答题')
            self._run_challenge()
        else:
            logger.info(f'未选择执行挑战答题')

        # 退出我要答题
        sleep(2)
        self._fresh()
        pos = self.xm.pos(cfg.get(self.rules, 'rule_quiz_exit'))
        self.ad.tap(pos)
        sleep(2)

        # 点击HOME
        self._fresh()
        pos = self.xm.pos(cfg.get(self.rules, 'rule_bottom_work'))
        self.ad.tap(pos)
