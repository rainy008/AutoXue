#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: quizXue
@file: main.py
@author: kessil
@contact: https://github.com/kessil/quizXue/
@time: 2019年07月26日 15:00:59
@desc: Life is short, you need Python
'''
from time import sleep
from argparse import ArgumentParser
from configparser import ConfigParser
from random import randint
from urllib.parse import quote
from playsound import playsound
from model import Model, Bank
from adble import Adble
import re
import threading
import requests
import string

def attention(filename='attention.mp3', repeat=2):
    '''语音提示：https://developer.baidu.com/vcast导出音频'''
    for i in range(repeat):
        playsound('./sounds/%s'%filename)

def search(question):
    '''搜索引擎检索题目'''
    content = re.sub(r'[\(（]出题单位.*', "", question.content)
    print(content)
    url = quote('https://www.baidu.com/s?wd=' + content, safe=string.printable)
    response = requests.get(url, headers=headers).text
    if question.item1: print('A. %s: %d'%(question.item1, response.count(question.item1)))
    if question.item2: print('B. %s: %d'%(question.item2, response.count(question.item2)))
    if question.item3: print('C. %s: %d'%(question.item3, response.count(question.item3)))
    if question.item4: print('D. %s: %d'%(question.item4, response.count(question.item4)))
    print('%s\n请先在手机提交答案，根据提交结果输入答案！'%('-'*min(len(question.content)*2, 120)))


def start(device, count=None):
    m_ad = Adble(device)
    m_db = Model()

    cfg = ConfigParser()
    cfg.read('./config.ini')
    if not count: count = cfg.getint('base', 'answer_count')
    delay_rand = cfg.getboolean('base', 'delay_rand')
    delay = 1
    for i in range(count):
        xml = m_ad.get_xml()
        question = Bank.from_xml(device)
        bank = m_db.query(content=question.content)
        if delay_rand: 
            delay = randint(1,6)

        if bank:
            index = ord(bank.answer)-65
            pos = complex(question.bounds.split(' ')[index])
            print(bank)
            print(f"\n {delay} 秒自动提交答案:  {bank.answer}\n")
            if 0j == pos:
                t= threading.Thread(target=attention, args=('crossed.mp3',1))#创建线程
                t.start()
                sleep(5)
                continue
            else:
                sleep(delay)
                m_ad.tap(int(pos.real), int(pos.imag))
        else:
            t= threading.Thread(target=attention, args=('doubt.mp3',2))#创建线程
            t.start()
            headers = {
                'User-Agent': cfg.get('base', 'user_agent')
            }
            search(question, headers)
            ch = input('请输入：').upper()
            if ch and 'N' == ch:
                break
            if ch and ch in "ABCD":
                question.answer = ch
                m_db.add(question)


if __name__ == "__main__":
    parse = ArgumentParser(description='学习强国挑战答题助手')
    parse.add_argument('-d', '--device', metavar='device',default='mumu', help='指定一中终端类型，不同终端对应不同的xpath规则')
    # parse.add_argument('-c', '--count', metavar='count',default='30', help='指定答题数量')
    args = parse.parse_args()

    start(args.device)