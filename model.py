#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: quizXue
@file: model.py
@author: kessil
@contact: https://github.com/kessil/quizXue/
@time: 2019年07月26日 12:05:41
@desc: Life is short, you need Python
'''
import re
from sqlalchemy import Column,Integer, String, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from lxml import etree
from configparser import ConfigParser

# 创建对象的基类:
Base = declarative_base()

# 定义Bank对象:
class Bank(Base):
    # 表的名字:
    __tablename__ = 'Bank'

    # 表的结构:
    id = Column(Integer,primary_key=True)
    content = Column(Text, unique=True)
    item1 = Column(String(128))
    item2 = Column(String(128))
    item3 = Column(String(128))
    item4 = Column(String(128))
    answer = Column(String(8))
    bounds = Column(String(64))

    def __init__(self, content, options, answer='', bounds=''):
        for i in range(len(options), 4):
            options.append('')
        # print(options)
        self.content = content
        self.item1, self.item2, self.item3, self.item4 = [str(x) for x in options]
        self.answer = answer
        self.bounds = bounds

    @classmethod
    def from_xml(cls, device='mumu'):
        # print("device", device)
        cfg = ConfigParser()
        cfg.read('./config.ini')
        filename = cfg.get(device, 'xml_uri')
        # print(f'Parse {filename}……')
        xml = etree.parse(filename)
        root = xml.getroot()
        xml_question = root.xpath(cfg.get(device, 'question'))[-1]
        content = xml_question.xpath(cfg.get(device, 'question_content'))[0]
        # print(content)
        xml_options = xml_question.xpath(cfg.get(device, 'options'))
        options = [x.xpath(cfg.get(device, 'option_content'))[0] for x in xml_options]
        # print(options)
        bounds = []
        for x in xml_options:
            ''' 此处保存的bounds针对华为P20 分辨率2244*1080'''
            x0, y0, x1, y1 = [int(x) for x in re.findall(r'\d+', x.xpath(cfg.get(device, 'option_bounds'))[0])]
            pos = complex((x0+x1)/2, (y0+y1)/2)
            bounds.append(pos)
        bounds = " ".join([str(x) for x in bounds])
        # print(bounds)
        return cls(content=content, options=options, bounds=bounds)

    def __eq__(self, other):
        return self.content == other.content
    
    def __repr__(self):
        return f'<Bank {self.id}>'
    
    def __str__(self): 
        # 统一题目内容的留空为两个英文下划线
        # 江南自古富庶地，风流才子美名扬，江南四大才子是__、__、__、__。 
        # 油锅起火时使用以下方法中__方法扑灭是不正确的。
        content = re.sub(r'[\(（]出题单位.*', "", self.content)
        content = re.sub(r'(\s{2,})|(（\s*）)|(【\s*】)', '____', content)
        items = [x for x in (self.item1, self.item2, self.item3, self.item4) if x]
        # items = ['%c. %s'%(chr(i+65), x) for (i,x) in enumerate(items) if x]
        if self.answer:
            index = ord(self.answer)-65
            if index < len(items):
                items[index] = f'**{items[index]}**'
            answer = f'**{self.answer.upper()}**'
        else:
            answer = ''
        options = '\n'.join([f'+ {x}' for x in items])
        return f'{self.id}. {content} {answer}\n{options}\n'


class Model():
    def __init__(self):
        cfg = ConfigParser()
        cfg.read('./config.ini')
        database_uri = cfg.get('database', 'database_uri')
        # 初始化数据库连接:
        engine = create_engine(database_uri)
        # 创建DBSession类型:
        Session = sessionmaker(bind=engine)

        Base.metadata.create_all(engine)
        self.session = Session()

    def query(self, id=None, content=None):
        '''数据库检索记录'''
        if id and isinstance(id, int):
            return self.session.query(Bank).filter_by(id=id).first()
        if content and isinstance(content, str):
            return self.session.query(Bank).filter_by(content=content).first()
        return self.session.query(Bank).all()

    def add(self, item):
        '''数据库添加纪录'''
        result = self.query(content=item.content)
        if result:
            print(f'数据库已存在此纪录，无需添加纪录！')
        else:
            self.session.add(item)
            self.session.commit()
            print(f'数据库添加记录成功！')

    def delete(self, item):
        '''数据库删除记录'''
        to_del = self.qeury(content=item.content)
        if to_del:
            session.delete(to_del)
            session.commit()
        else:
            print('数据库无此纪录!')

    def update(self, id, answer):
        '''数据库更新记录'''
        to_update = self.query(id=id)
        if to_update:
            to_update.answer = answer
            session.commit()
            print(f'更新题目[{id}]的答案为“{answer}”')
        else:
            print('数据库无此纪录!')

    def export_markdown(self, filename):
        data = self.query()
        if not data:
            raise 'database is empty'
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(f'# 学习强国题库： {len(data)}\n')
            for item in data:
                fp.write(str(item))
        print(f'题库已导出到{filename}')
    
    def export_excel(self, filename):
        import xlwt
        data = self.query()
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('题库')
        if not data:
            raise 'database is empty'
        ws.write(0, 0, '序号')
        ws.write(0, 1, '题目')
        ws.write(0, 2, '选项A')
        ws.write(0, 3, '选项B')
        ws.write(0, 4, '选项C')
        ws.write(0, 5, '选项D')
        ws.write(0, 6, '答案')
        for d in data:
            ws.write(d.id, 0, label=d.id)
            ws.write(d.id, 1, label=d.content)
            ws.write(d.id, 2, label=d.item1)
            ws.write(d.id, 3, label=d.item2)
            ws.write(d.id, 4, label=d.item3)
            ws.write(d.id, 5, label=d.item4)
            ws.write(d.id, 6, label=d.answer)
        wb.save(filename)
        print('题库已导出到%s'%filename)

if __name__ == "__main__":
    db = Model()
    # for d in db.query():
    #     print(d)
    # db.export_markdown('./data/data-dev.md')
    db.export_excel('./data/data-dev.xls')
