#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@file: main.py
@author: kessil
@contact: https://github.com/kessil/
@time: 2019年06月02日 15:58:23
@desc: Life is short, you need Python
'''
from time import sleep
from adble import pull_xml, tap_screen
from model import Base, engine, Session,Bank, db_add, db_qeury
import requests
import string
from urllib.parse import quote
from config import Config
import re
from playsound import playsound
import threading
from random import randint

filename = Config.XML_URI
question = None
Base.metadata.create_all(engine)
session = Session()

def attention(filename='attention.mp3', repeat=Config.REPEAT_TIMES):
    '''语音提示：https://developer.baidu.com/vcast导出音频'''
    for i in range(repeat):
        playsound('./sounds/%s'%filename)

def search(question):
    '''搜索引擎检索题目'''
    content = re.sub(r'[\(（]出题单位.*', "", question.content)
    url = quote('https://www.baidu.com/s?wd=' + content, safe=string.printable)
    headers = Config.HEADERS
    response = requests.get(url, headers=headers).text
    if question.item1: print('A. %s: %d'%(question.item1, response.count(question.item1)))
    if question.item2: print('B. %s: %d'%(question.item2, response.count(question.item2)))
    if question.item3: print('C. %s: %d'%(question.item3, response.count(question.item3)))
    if question.item4: print('D. %s: %d'%(question.item4, response.count(question.item4)))
    print('%s\n请先在手机提交答案，根据提交结果输入答案！'%('-'*min(len(question.content)*2, 120)))
    

def run(session, num=float('inf')):
    # t= threading.Thread(target=attention)#创建线程
    # t.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
    while num:
        num = num - 1
        pull_xml(filename)
        sleep(1)
        question = Bank.from_xml(filename)
        print('\n%s\n%s'%('-'*min(len(question.content)*2, 120), question.content))
        bank = db_qeury(session, content=question.content)
        delay = 1 # randint(3,5)
        if bank:
            index = ord(bank.answer)-65
            pos = complex(question.bounds.split(' ')[index])
            if question.item1: print('A. %s'%question.item1)
            if question.item2: print('B. %s'%question.item2)
            if question.item3: print('C. %s'%question.item3)
            if question.item4: print('D. %s'%question.item4)
            print(f"\n {delay} 秒自动提交答案:  {bank.answer}\n")
            if 0j == pos:
                t= threading.Thread(target=attention, args=('crossed.mp3',1))#创建线程
                t.start()
                sleep(5)
                continue
            else:
                sleep(delay)
                tap_screen(int(pos.real), int(pos.imag))
        else:
            t= threading.Thread(target=attention, args=('doubt.mp3',2))#创建线程
            t.start()
            search(question)
            ch = input('请输入：').upper()
            if ch and 'N' == ch:
                break
            if ch and ch in "ABCD":
                question.answer = ch
                db_add(session, question)

        

if __name__ == "__main__":
    run(session, 35)