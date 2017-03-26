# -*- coding: utf-8 -*-
'''
单线程测试
'''

import csv
import re
import lxml.html
from link_crawler import link_crawler
from mongo_cache import MongoCache


class ScrapeCallback:
    '''略
    '''
    def __init__(self):
        self.writer = csv.writer(open('lianjia.csv', 'w'))
        self.fields = ('单价')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/ershoufang/sh[0-9]+.html', url):
            #html = html.decode('utf-8') #python3
            tree = lxml.html.fromstring(html)
            row = []
            # div > div#price > span.unit
            unit = tree.cssselect('table.aroundInfo > tr > td')[0].text_content()
            unit = unit.replace(' ', '')
            row.append(unit.replace('\n', ''))
            self.writer.writerow(row)

def lianjia():
    '''链家爬虫
    http://sh.lianjia.com/ershoufang/d1rs
    '''
    seed_url = "http://sh.lianjia.com/ershoufang/d1rs"
    link_crawler(seed_url, '/ershoufang/sh[0-9]+.html',
                 cache=MongoCache(),
                 scrape_callback=ScrapeCallback())


if __name__ == '__main__':
    lianjia()
