# coding:utf8

'''
    根据电影id获取详细信息
'''

import urllib.request, urllib.error, urllib.parse
import time
from bs4 import BeautifulSoup
import mysql.connector
from .dbTool import *

config = {
    'host': '119.29.32.91',
    'user': 'cjj',
    'password': 'ZHANGxj9469',
    'port': 3306,
    'database': 'video',
    'charset': 'utf8'
}

#connect MySQL
def mysql_conn():
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect error!{}'.format(e))
        return None
    else:
        #print('connect success!')
        return conn

#close connector
def mysql_close(conn):
    '''
    :param conn: mysql_connector
    :return:
    '''
    if conn.is_connected:
        conn.close()

    #print('connect close!')

#MySQL select
def mysql_sel(conn, sqlStr, param):
    '''
    :param conn: mysql_connector
    :param sqlStr: sql命令
    :param param: 参数
    :return: results or None
    '''
    if not conn.is_connected():
        print("Connection is disconnected")
        return None
    cursor = conn.cursor()
    #print(sqlStr+str(param))
    try:
        cursor.execute(sqlStr, param)
        results = cursor.fetchall()
    except mysql.connector.Error as e:
        print('query error!{}'.format(e))
        return None
    else:
        return results
    finally:
        cursor.close()

#Mysql insert
def mysql_ins(conn, sqlStr, param):
    '''
    :param conn: mysql_connector
    :param sqlStr: sql命令
    :param param: 参数
    :return: 0失败/1成功
    '''
    if not conn.is_connected():
        print("Connection is disconnected")
        return 0
    cursor = conn.cursor()
    # print(sqlStr+str(param))
    try:
        cursor.execute(sqlStr, param)
        conn.commit()
    except mysql.connector.Error as e:
        print('insert error!{}'.format(e))
        conn.rollback()
        return 0
    else:
        return 1
    finally:
        cursor.close()

inputFile = 'douban_movie.txt'
fr = open(inputFile, 'r')

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

firstLine = True
count = 1
errorCount = 0
result = {}

# 读取数据库电影id到数组
conn = mysql_conn()
for line in fr:
    if firstLine:
        firstLine = False
        continue

    line = line.split(';')
    movieId = line[0]
    title = line[1]
    url = line[2]
    cover = line[3]
    rate = line[4].rstrip('\n')
    if rate=='':
        rate=0

    sql = 'select id from movie where id=%s'
    param = (movieId,)
    result_list = mysql_sel(conn, sql, param)
    if movieId in result or len(result_list)!=0:
        print(title,'--重复')
        continue
    else:
        result[str(movieId)] = 1

    try:
        request = urllib.request.Request(url=url,headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read()
        html = BeautifulSoup(html, 'html.parser')
        info = html.select('#info')[0]
        info = info.get_text().split('\n')
        imagUrl = ''
        for child_img in html.select('#related-pic')[0].ul.select('li'):
            imagUrl += child_img.select('a')[0].img['src'] + ';'

        # 提取字段，只要冒号后面的文本内容
        newInfo = {'director': '', 'composer': '', 'actor': '', 'category': '', 'district': '', 'language': '',
                   'showtime': '', 'episode': '', 'length': '', 'othername': ''}
        for i in range(len(info)):
            if info[i].split(':')[0].strip() == '导演':
                newInfo['director'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '编剧':
                newInfo['composer'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '主演':
                newInfo['actor'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '类型':
                newInfo['category'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '制片国家/地区':
                newInfo['district'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '语言':
                newInfo['language'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '上映日期':
                newInfo['showtime'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '首播':
                newInfo['showtime'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '片长':
                newInfo['length'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '单集片长':
                newInfo['length'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '又名':
                newInfo['othername'] = info[i].split(':')[1].strip()
                continue
            if info[i].split(':')[0].strip() == '集数':
                newInfo['episode'] = info[i].split(':')[1].strip()
                continue
        director = newInfo['director']
        composer = newInfo['composer']
        actor = newInfo['actor']
        category = newInfo['category']
        district = newInfo['district']
        language = newInfo['language']
        showtime = newInfo['showtime']
        length = newInfo['length']
        othername = newInfo['othername']
        if html.select('div[class="gtleft]"')[0].span.a['data-type'] == '电视剧':
            print(count,'--电视剧--' + title + '\t' + movieId)
            episode = newInfo['episode']
        else:
            print(count,'--电影--' + title + '\t' + movieId)
            episode = 0

    # 电影简介
        description = html.find_all("span", attrs={"property": "v:summary"})[0].get_text()
        description = description.lstrip().lstrip('\n\t').rstrip().rstrip('\n\t').replace('\n','\t')
        print(director)
        print(director.encode('utf8'))
        # 写入数据
        record = str(movieId) + '^' + title + '^' + url + '^' + cover + '^' + str(rate) + '^' + director + '^' + composer + '^' + actor+ '^' + category + '^' + district+ '^' + language + '^' + showtime + '^' + str(episode) +'^' + length + '^' + othername + '^' + description +'^' + imagUrl + '\n'
        sql = 'insert into movie values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        param = (str(movieId),title,url,cover,float(rate),director,composer,actor, category, district,language,showtime, str(episode),length,othername,description,imagUrl)
    except Exception as e:
        print(e)
        print(count,title,"Error")
        errorCount = errorCount + 1
    else:
        mysql_ins(conn, sql, param)
    finally:
        time.sleep(3)
    count = count + 1

mysql_close(conn)
print(count, errorCount)
fr.close()