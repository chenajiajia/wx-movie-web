#!/usr/bin/env python
# coding:utf8

'''
    根据电影id获取详细信息
    author: Honlan
    email: 493722771@qq.com
    date: 2015/09/06
'''

import urllib.request, urllib.error, urllib.parse
import time
from bs4 import BeautifulSoup
import re

def getEp(title):
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    url = 'https://so.360kan.com/index.php?kw=' + urllib.parse.quote(title) + '&from='
    request = urllib.request.Request(url=url, headers=headers)
    # request = urllib2.Request(url=url)
    response = urllib.request.urlopen(request)
    html = response.read()
    html = BeautifulSoup(html, 'html.parser')
    info = html.find("div", class_="cont").find('ul').find('li').find('span').string
    result = re.sub("\D", "", info)
    return result