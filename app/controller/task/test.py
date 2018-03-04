import urllib.request, urllib.error, urllib.parse
import requests
from bs4 import BeautifulSoup
import re
import time
import socket
from retrying import retry
import mysql.connector

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

# Mysql update
def mysql_upd(conn, sqlStr, param):
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
        print('update error!{}'.format(e))
        conn.rollback()
        return 0
    else:
        return 1
    finally:
        cursor.close()

# headers = {}
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                         'Chrome/64.0.3282.168 Safari/537.36',
#            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#            'Accept-Language':'zh-CN,zh;q=0.9',
#            'Connection':'close'}

# while(1):
#     start = time.clock()
#     s = requests.Session()
#     try:
#         request = s.get(url=url, headers=headers, timeout=4, verify=False)
#         html = BeautifulSoup(request.text, 'html.parser')
#         info = html.find("div", class_="cont").find('ul').find('li').find('span').string
#         result = re.sub("\D", "", info)
#         print(result)
#     except Exception as e:
#         print(str(e))
#         end = time.clock()
#         print("Running time: %s Seconds" % (end - start))
#         time.sleep(3)

#判断是否是异常
def retry_if_urllib_error(exception):
    return isinstance(exception, Exception)

#当发生异常时会重试获取集数，重试次数stop_max_attempt_number为5
@retry(retry_on_exception=retry_if_urllib_error, stop_max_attempt_number=5)
def getEp(title):
    url = 'https://so.360kan.com/index.php?kw=' + urllib.parse.quote(title)
    timeout = 4
    socket.setdefaulttimeout(timeout)
    response = urllib.request.urlopen(url=url, timeout=4)
    html = response.read()
    html = BeautifulSoup(html, 'html.parser')
    info = html.find("div", class_="cont").find('ul').find('li').find('span').string
    result = re.sub("\D", "", info)
    if result == '':
        result = '0'
    return int(result)
    # raise urllib.error.URLError('info')
    # raise urllib.error.HTTPError('info')
    # raise socket.timeout('info')

if __name__ == '__main__':
    start = 0
    while True:
        conn = mysql_conn()
        sql = 'select distinct video_id, update_episode, title from subscription,movie where video_id=' \
              'movie.id and update_episode<subscription.episode limit %s,%s'
        param = (start,10)
        result_list = mysql_sel(conn, sql, param)
        for row in result_list:
            movieId = row[0]
            update_episode = row[1]
            title = row[2]
            new_episode = 0
            try:
                new_episode = getEp(title)
                print('new_episode:',new_episode)
            except Exception as e:
                print(str(e))
            if update_episode<new_episode:
                sql = 'update subscription set is_update=%s, update_episode=%s where video_id=%s'
                param = (1, new_episode, movieId)
                mysql_upd(conn, sql, param)
            time.sleep(1)
        mysql_close(conn)
        start = start + 10
        if len(result_list)<10:
            break


