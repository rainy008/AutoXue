#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: quizXue
@file: reader.py
@author: kessil
@contact: https://github.com/kessil/quizXue/
@time: 2019-08-09(星期五) 12:01
@Copyright © 2019. All rights reserved.
'''
from time import sleep
from .. import logger, cfg

class Reader:
    '''设计思路：
        1. 点击Home，找到‘发布’栏拖到‘推荐’栏处，此时订阅栏出现
        2. 点击订阅栏，下拉刷新
        3. 保存第一个Item坐标
        4. 依次学习后续可点击Item（第二个开始），将最后一个Item拉至第一个Item处
        5. 在第一轮阅读中插入收藏、分享、评论操作
        6. 重复步骤4直到完成指定篇数新闻阅读
        7. 退出文章学习（其实不用退出，本来就在Home页
    '''
    def __init__(self, rules, ad, xm):
        self.rules = rules
        self.ad = ad
        self.xm = xm

        self.home = 0j
        self.feeds = 0j

    def _fresh(self):
        sleep(1)
        self.ad.uiautomator()
        self.xm.load()

    def enter(self):
        # 进入‘订阅’，要求用户首先订阅公号
        self._fresh()
        home = self.xm.pos(cfg.get(self.rules, 'rule_bottom_work'))

