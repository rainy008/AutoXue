#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: StudyEveryday
@file: challenge.py
@author: kessil
@contact: https://github.com/kessil/StudyEveryday/
@time: 2019-08-01(星期四) 20:55
@Copyright © 2019. All rights reserved.
'''
import os
import re
import json
import requests
import string
from random import randint
from urllib.parse import quote
from time import sleep
from ..model import Bank, Model
from .. import logger, cfg


class ChallengeQuiz(object):
    def __init__(self, rules, ad, xm):
        self.rules = rules
        self.filename = cfg.get('common', 'challenge_json')
        self.ad = ad
        self.xm = xm
        self.db = Model(cfg.get('common', 'database_challenge'))
        self.has_bank = False
        self.is_user = cfg.getboolean('common', 'is_user')
        self.json_blank = self._load()
        self.content = ''
        self.options = ''
        self.answer = ''
        self.pos = ''
        self.p_back = 0j
        self.p_return = 0j
        self.p_share = 0j

    def _enter(self):
        self._fresh()
        pos = self.xm.pos(cfg.get(self.rules, 'rule_challenge_entry'))
        self.ad.tap(pos)
        sleep(2)

    def _fresh(self):
        self.ad.uiautomator()
        self.xm.load()

    def _load(self):
        '''load json file'''
        filename = self.filename
        res = []
        if(os.path.exists(filename)):
            with open(filename,'r',encoding='utf-8') as fp:
                try:
                    res = json.load(fp)
                except Exception:
                    logger.debug(f'加载JSON数据失败')
                logger.debug(res)
            logger.info(f'载入JSON数据{filename}')
            return res
        else:
            logger.debug('JSON文件{filename}不存在')
            return res
        

    def _dump(self):
        '''save json file'''
        filename = self.filename
        with open(filename,'w',encoding='utf-8') as fp:
            json.dump(self.json_blank,fp,indent=4,ensure_ascii=False)
        logger.info(f'导出JSON数据{filename}')
        return True

    def _search(self):
        logger.debug(f'search - {self.content}')
        '''搜索引擎检索题目'''
        content = re.sub(r'[\(（]出题单位.*', "", self.content)
        logger.info(f'\n{content}')
        url = quote('https://www.baidu.com/s?wd=' + content, safe=string.printable)
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        response = requests.get(url, headers=headers).text
        counts = []
        for i, option in enumerate(self.options.split(' ')):
            count = response.count(option)
            counts.append(count)
            itemname = chr(i+65)
            logger.info(f'{itemname}. {option}: {count}')

        max_index = counts.index(max(counts))
        self.answer = chr(max_index+65)
        return max_index
        



    def _content(self):
        res = self.xm.content(cfg.get(self.rules, 'rule_challenge_content'))
        logger.debug(res)
        return res
    
    def _optoins(self):
        res = self.xm.options(cfg.get(self.rules, 'rule_challenge_options_content'))
        logger.debug(res)
        return res

    def _pos(self):
        res = self.xm.pos(cfg.get(self.rules, 'rule_challenge_options_bounds'))
        logger.debug(res)
        return res

    def _submit(self):
        challenge_delay = cfg.getint('common', 'challenge_delay')        
        if 0 == challenge_delay:
            delay_seconds = randint(0, 5)
        else:
            delay_seconds = challenge_delay
        self._fresh()
        self.content = self._content()
        self.options = self._optoins()
        self.pos = self._pos()
        options = "\n".join([f' - {x}' for x in self.options.split(' ')])
        print(f'\n[挑战题] {self.content[:45]}...\n{options}')
        bank = self.db.query(content=self.content, catagory='挑战题')
        if bank is not None:
            self.has_bank = True
            logger.debug('bank from database')
            cursor = ord(bank.answer) - 65
            sleep(delay_seconds) # 延时按钮
        else:
            self.has_bank = False
            cursor = self._search()
            
        logger.debug(f'正确选项下标 {cursor}')
        # 点击正确选项
        wm = self.ad.wm_size() # example: [1024, 576]
        x0 = wm[1]//2
        y0 = wm[0]//3*2
        while 0j == self.pos[cursor]:
            self.ad.swipe(x0, y0, x0, y0-200, 500)
            self._fresh()
            self.pos = self._pos()
        # 现在可以安全点击(触摸)
        self.ad.tap(self.pos[cursor])

    
    def _return(self):
        self.ad.back()
   
    def _db_add(self):
        # from_challenge(cls, content, options, answer='', bounds='')
        if not self.has_bank:
            bank = Bank.from_challenge(content=self.content, options=self.options, answer=self.answer, bounds='')
            self.db.add(bank)
            

    def _reopened(self, repeat:bool=False)->bool:
        sleep(2)
        self._fresh()
        # 本题答对否
        if not self.xm.pos(cfg.get(self.rules, 'rule_judge_bounds')):
            self._db_add()
            return True
        
        # 分享复活否？
        pos = self.xm.pos(cfg.get(self.rules, 'rule_share_bounds'))
        if pos:
            self._commet()
            logger.debug('点击分享复活')
            logger.info('复活中，请稍等...')            
            self.ad.tap(pos)
            self._return()
            sleep(5)
            self._fresh()
            return True
        
        # 再来一局否？
        pos = self.xm.pos(cfg.get(self.rules, 'rule_again_bounds'))
        if pos:
            self._commet()
            if repeat:
                logger.debug('点击再来一局')
                logger.info('开局中，请稍等...')
                sleep(10) # 平台奇葩要求，10秒内仅可答题一次
                self.ad.tap(pos)
                sleep(5)
                return True
            else:
                self._return()
                return False
        return True

    def _commet(self):
        maxlen = len(self.options)
        try:
            ch = input(f'请输入正确的答案: ').upper()
            assert ch in 'NABCD'[:maxlen+1],f"输入的项目不存在，请输入A-DN"
        except Exception as ex:
            print(f"输入错误:",ex)
        if ch in 'ABCD':
            self.answer = ch
            self._db_add()
        return ch
            

    def run(self, count):
        self._enter()
        while count:
            self._submit()
            if self._reopened(False): # 回答正确
                count = count - 1
            else:
                break
        logger.info(f'已达成目标题数，等30秒后退出')
        sleep(30)
        self._return()
        self._dump()
        return count


