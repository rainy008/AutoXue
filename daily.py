#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: quizXue
@file: daily.py
@author: kessil
@contact: https://github.com/kessil/quizXue/
@time: 2019-07-27(星期六) 21:46
@Copyright © 2019. All rights reserved.
'''
import re
from time import sleep
from lxml import etree
from configparser import ConfigParser
from adble import Adble

class Daily(object):
    def __init__(self):
        print('running init func...')
        cfg = ConfigParser()
        cfg.read('./default.ini', encoding='utf-8')
        cfg.read('./user.ini', encoding='utf-8')
        self.filename = cfg.get('daily', 'xml_uri')
        self.duration = cfg.getint('daily', 'duration')
        self.repeat = cfg.getint('daily', 'repeat')
        self.paper = cfg.getint('daily', 'paper')
        self.question_type = cfg.get('daily', 'question_type')
        self.choice_content = cfg.get('daily', 'choice_content')
        self.options_bounds = cfg.get('daily', 'options_bounds')
        self.blank_content = cfg.get('daily', 'blank_content')
        self.edit_bounds = cfg.get('daily', 'edit_bounds')
        self.desc_content = cfg.get('daily', 'desc_content')
        self.btn_submit = cfg.get('daily', 'btn_submit')
        self.back_bounds = cfg.get('daily', 'back_bounds')
        self.home_bounds = cfg.get('daily', 'home_bounds')
        self.correct_content = cfg.get('daily', 'correct_content')
        self.btn_goback = cfg.get('daily', 'btn_goback')
        self.btn_goon = cfg.get('daily', 'btn_goon')
        self.news_goto_study = cfg.get('daily', 'news_goto_study')
        self.goto_quiz = cfg.get('daily', 'goto_quiz')
        self.goto_daily_quiz = cfg.get('daily', 'goto_daily_quiz')

        self.ad = Adble(device='daily')
        self.content = ''
        self.answer = ''
        self.pos_submit = 0j
        self.pos_home = 0j
        self.pos_back = 0j
        self.remember = False


    def _get_bounds(self, rules, remember=False):
        '''将获取点击位置的操作抽象为一个函数
            输入： xpath规则
            返回： 位置list（复数形式表示），为什么是list？因为多选题
        '''
        if not remember:
            self.ad.get_xml(self.filename)
        xml = etree.parse(self.filename)
        root = xml.getroot()
        bounds = root.xpath(rules)
        # print(bounds)
        result = []
        for bound in bounds:
            x0, y0, x1, y1 = [int(x) for x in re.findall(r'\d+', bound)]
            pos = complex((x0+x1)//2, (y0+y1)//2)
            # print(pos)
            result.append(pos)
        # print(f'get_bounds: {result}')
        return result

    def _get_content(self, rules, remember=False):
        '''获取文本内容'''
        print('exec _get_content func')
        if not remember:
            self.ad.get_xml(self.filename)
        xml = etree.parse(self.filename)
        root = xml.getroot()
        texts = root.xpath(rules)
        # print(texts)
        # for text in texts:
        #     print(text.xpath('./@content-desc'))
        result = ' '.join(texts)
        # print(f'get_content: {result}')
        return result

    def _get_node_count(self, rules, remember=False):
        '''获取节点数量'''
        print('exec _get_content func')
        if not remember:
            self.ad.get_xml(self.filename)
        xml = etree.parse(self.filename)
        root = xml.getroot()
        nodes = root.xpath(rules)
        # print(f'get_node_count: {count}')
        return count

    def enter(self):
        '''进入每日答题'''
        '''分三步：点击<我的>或<我要学习>, 点击<我要答题>， 点击<每日答题>
        '''
        print('running enter func...')

        # step 1
        self.pos_home = self._get_bounds(self.home_bounds)[0]
        pos = self._get_bounds(self.news_goto_study, True)[0]        
        self.ad.tap(pos.real, pos.imag)
        sleep(1)

        # step 2
        pos = self._get_bounds(self.goto_quiz)[0]
        self.ad.tap(pos.real, pos.imag)
        sleep(1)

        # step 3
        self.pos_back = self._get_bounds(self.back_bounds)[0]
        pos = self._get_bounds(self.goto_daily_quiz, True)[0]
        self.ad.tap(pos.real, pos.imag)
        sleep(1)




    
    def gohome(self):
        '''退出每日答题'''
        print('running gohome func...')
        if 0j != self.pos_back:
            self.ad.tap(self.pos_back.real, self.pos_back.imag)
        sleep(1)
        if 0j != self.pos_home:
            self.ad.tap(self.pos_home.real, self.pos_home.imag)        



    def dispatch(self):
        '''判断题目类型并分派'''
        print('running dispatch func...')
        while True:
            for i in range(self.paper):
                questype = self._get_content(self.question_type)
                print(questype)
                if '填空题' == questype:
                    self.blank()
                elif '单选题' == questype:
                    self.radio()
                elif '多选题' == questype:
                    self.check()
                else:
                    print('未知题目类型')

            correct = self._get_content(self.correct_content, False)
            print(f'回答正确题数：{correct}')
            if '5' == correct:
                self.repeat = self.repeat - 1
            self.repeat = self.repeat - 1
            if self.repeat <= 0:
                goback = self._get_bounds(self.btn_goback, True)[0]
                self.ad.tap(goback.real, goback.imag)
                break
            else:
                goon = self._get_bounds(self.btn_goon, True)[0]
                self.ad.tap(goon.real, goon.imag)
                sleep(self.duration)
                continue



        

            
            


    def radio(self, remember=False):
        '''单选题'''
        print('running radio func...')
        self.content = self._get_content(self.choice_content, remember)
        print(self.content)
        pos_options = self._get_bounds(self.options_bounds, remember)
        print(pos_options)
        self.ad.tap(pos_options[0].real, pos_options[0].imag)
        sleep(2)
        self.submit()
        self.desc()
    



    def check(self, remember=False):
        '''多选题'''
        print('running check func...')
        self.content = self._get_content(self.choice_content, remember)
        print(self.content)
        pos_options = self._get_bounds(self.options_bounds, remember)
        print(pos_options)
        for pos in pos_options:
            if 0j != pos:
                self.ad.tap(pos.real, pos.imag)

        sleep(2)
        self.submit()
        self.desc()


    def blank(self, remember=False):
        '''填空题'''
        print('running blank func...')
        self.content = self._get_content(self.blank_content, remember)
        edit_areas = self._get_bounds(self.edit_bounds, True)
        # print(edit_areas)
        # blank_count = self._get_node_count('//node[@class="android.webkit.WebView"]/node[@class="android.webkit.WebView"]/node[last()]/node[@index="2"]/node[@class="android.widget.EditText"]/following-sibling::node[@content-desc=""]', True)
        # print(blank_count)
        for area in edit_areas:
            self.ad.tap(area.real, area.imag)
            self.ad.text('0')
            sleep(1)
        self.submit()
        self.desc()

    def submit(self):
        '''提交答案（或下一题）'''
        print('running submit func...')
        if 0j ==  self.pos_submit:
            self.pos_submit = self._get_bounds(self.btn_submit)[0]
        self.ad.tap(self.pos_submit.real, self.pos_submit.imag)

    def desc(self):
        # 获取答案或进入下一题
        sleep(1)
        desc = self._get_content(self.desc_content, False)
        
        if len(desc):
            '''答错了'''
            self.answer = re.sub(r'正确答案：', '', desc.strip())
            print(f'回答错误，正确答案是：{self.answer}')
            # 这里进行答案保存 self.content self.answer
            self.submit()
        else:
            '''答对了'''
            print('回答正确，下一题')
    
    def start(self):
        '''开始答题，每日回答六套题可得6分'''
        print('running start func...')
        self.enter()
        self.dispatch()
        self.gohome()

    def test(self):
        
        self.pos_back = self._get_bounds(self.back_bounds)[0]
        print(self.pos_back)
        if 0j != self.pos_back:
            self.ad.tap(self.pos_back.real, self.pos_back.imag)
        sleep(1)

        self.pos_home = self._get_bounds(self.home_bounds)[0]        
        print(self.pos_home)
        if 0j != self.pos_home:
            self.ad.tap(self.pos_home.real, self.pos_home.imag)  

if __name__ == "__main__":
    daily = Daily()
    daily.start()
    # daily.test()
