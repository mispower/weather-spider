# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from tools import spider_request
import re

target_url = 'http://www.xicidaili.com/nn'
regex = '<tr class=\"odd\">(.|\n)+(.|\n)</tr>'
doc = BeautifulSoup(spider_request.open_url(target_url), "lxml")

hht = doc.find_all('tr')
for x in hht[1]:
    print(x)
    print(type(x))


def get_proxies():
    for i in range(2000):
        spider_request.open_url()
