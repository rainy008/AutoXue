#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: StudyEveryday
@file: xmler.py
@author: kessil
@contact: https://github.com/kessil/StudyEveryday/
@time: 2019-07-31(星期三) 15:15
@Copyright © 2019. All rights reserved.
'''

import re
from lxml import etree
from .. import logger


def str2complex(s):
    x0, y0, x1, y1 = [int(x) for x in re.findall(r'\d+', s)]
    logger.debug(f'({x0}, {y0}) -> ({x1}, {y1})')
    res = complex((x0+x1)//2, (y0+y1)//2)
    logger.debug(res)
    return res

class Xmler(object):
    def __init__(self, filename:str):
        self.filename = filename
        # self.load()

    def load(self):
        self.root = etree.parse(self.filename)

    def _texts(self, rule:str)->list:
        '''return list<str>'''
        # logger.debug(f'xpath texts: {rule}')
        res = [x.replace(u'\xa0', u' ') for x in self.root.xpath(rule)]
        res = [' ' if '' == x else x for x in res]
        logger.debug(res)
        return res

    def pos(self, rule:str)->list:
        '''return list<complex>'''
        logger.debug(rule)
        res = self._texts(rule)
        logger.debug(res)
        points = [str2complex(x) for x in res]
        if len(points) == 1:
            res = points[0]
        else:
            res = points
        logger.debug(res)
        return res

    def content(self, rule:str)->str:
        '''return str'''
        logger.debug(rule)
        # res = self._texts(rule) # list<str>
        # res = ' '.join([" ".join(x.split()) for x in self._texts(rule)])
        res = ''.join(self._texts(rule))
        logger.debug(res)
        return res

    def options(self, rule:str)->str:
        res = [re.sub(r'\s+', '、', x) for x in self.root.xpath(rule)]
        logger.debug(res)
        res = ' '.join(res)
        logger.debug(res)
        return res

    def count(self, rule:str)->int:
        '''return int'''
        logger.debug(rule)
        res = self.root.xpath(rule)
        return len(res)