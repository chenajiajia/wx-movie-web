# coding:utf8

'''
    一次性爬取豆瓣所有电影的概要信息
'''

import urllib.request, urllib.parse
import json
import time
from app.controller.util.dbTool import *

def getAllMovies():
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    outputFile = 'douban_movie.txt'
    fw = open(outputFile, 'w')
    fw.write('id;title;url;cover;rate\n')

    headers = {}
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip, deflate, sdch"
    headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2"
    headers["Connection"] = "keep-alive"
    headers["Host"] = "movie.douban.com"
    headers["Referer"] = "http://movie.douban.com/"
    headers["Upgrade-Insecure-Requests"] = 1
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gec" \
                            "ko) Chrome/45.0.2454.85 Safari/537.36"

    # 获取tag
    tags = ['剧情', '爱情', '喜剧', '科幻', '动作', '悬疑', '犯罪', '恐怖', '青春', '励志', '战争', '文艺', '黑色幽默',
            '传记', '情色', '暴力', '音乐', '家庭']

    # 开始爬取
    print("********** START **********")
    print(time.strftime(ISOTIMEFORMAT, time.localtime()))
    result = {}
    # 按标签tag获取视频
    for tag in tags:
        print("Crawl movies with tag: " + tag)
        print(time.strftime(ISOTIMEFORMAT, time.localtime()))

        start = 0
        flag = 0
        conn = mysql_conn()
        # sort=R按时间排序获取新的视频
        # 一直到获取到的视频在数据库中已存在则更换标签tag
        while True:
            time.sleep(5)
            url = "https://movie.douban.com/j/new_search_subjects?" \
                  "sort=R&range=0,10&tags=" + urllib.parse.quote(tag) + \
                  "&start=" + urllib.parse.quote(str(start))
            request = urllib.request.Request(url=url)
            response = urllib.request.urlopen(request)
            movies = json.loads(response.read().decode('utf8'))['data']
            if len(movies) == 0:
                print("movies is null")
                break
            for item in movies:
                time.sleep(3)
                rate = item['rate']
                title = item['title']
                url = item['url']
                cover = item['cover']
                movieId = item['id']
                # 判断数据库中是否已存在该视频
                sql = 'select id from movie where id=%s'
                param = (movieId,)
                result_list = mysql_sel(conn, sql, param)
                if len(result_list) != 0:
                    print('id:' + movieId + '--title:' + title + '--数据库存在')
                    flag = flag + 1
                    if flag > 15:
                        break
                    else:
                        continue
                else:
                    flag = 0
                if movieId in result:
                    print(title, '--重复')
                    continue
                else:
                    result[str(movieId)] = 1
                record = str(movieId) + ';' + title + ';' + url + ';' + cover + ';' + str(rate) + '\n'
                fw.write(record)
                print(tag + '\t' + title + '\t' + str(movieId))
            if flag > 15:
                break;
            start = start + 20
        mysql_close(conn)

    fw.close()
    print("           ------")
    print("        ------------")
    print("------getAllMovies over------")
    print("        ------------")
    print("           ------")
