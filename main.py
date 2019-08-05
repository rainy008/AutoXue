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

def search(question, headers):
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


def start(device, count, filename, database_uri, delay_seconds, user_agent):
    m_ad = Adble(device)
    m_db = Model(database_uri, 'data-dev')
    if 0 == delay_seconds:
        delay_rand = True
    else:
        delay_rand = False

    for i in range(count):
        xml = m_ad.get_xml(filename)
        question = Bank.from_xml(device)
        bank = m_db.query(content=question.content)
        if delay_rand: 
            delay_seconds = randint(1,6)

        if bank:
            index = ord(bank.answer)-65
            pos = complex(question.bounds.split(' ')[index])
            print(question)
            print(f"\n {delay_seconds} 秒自动提交答案:  {bank.answer}\n")
            if 0j == pos:
                t= threading.Thread(target=attention, args=('crossed.mp3',1))#创建线程
                t.start()
                sleep(5)
                continue
            else:
                sleep(delay_seconds)
                m_ad.tap(int(pos.real), int(pos.imag))
        else:
            t= threading.Thread(target=attention, args=('doubt.mp3',2))#创建线程
            t.start()
            headers = {
                'User-Agent': user_agent
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
    parse.add_argument('-d', '--device', metavar='device',default='phone', help='指定一中终端类型，不同终端对应不同的xpath规则')
    parse.add_argument('-c', '--count', metavar='count',default='35', help='指定答题数量')
    args = parse.parse_args()
    try:
        count_question = int(args.count)
    except Exception as e:
        print(e)

    # 读取系统配置和用户配置，后面加载的具有高优先级
    
    cfg = ConfigParser()
    cfg.read('./default.ini', encoding='utf-8')
    cfg.read('./user.ini', encoding='utf-8')

    device = args.device or cfg.get('base', 'device_type')
    count_question = count_question or cfg.get('base', 'count_question')
    filename = cfg.get(device, 'xml_uri')
    delay_seconds = cfg.getint('base', 'delay_seconds')
    user_agent = cfg.get('base', 'user_agent')   

    database_uri = cfg.get('database', 'database_uri')

    start(device, count_question, filename, database_uri, delay_seconds, user_agent)
