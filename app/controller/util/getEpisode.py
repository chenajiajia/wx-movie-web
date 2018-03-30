import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import re
import time
import socket
import ssl
from retrying import retry
from app.controller.util.dbTool import *

#判断是否是异常
def retry_if_urllib_error(exception):
    return isinstance(exception, Exception)

#当发生异常时会重试获取集数，重试次数stop_max_attempt_number为5
@retry(retry_on_exception=retry_if_urllib_error, stop_max_attempt_number=5)
def getEp(title):
    url = 'https://so.360kan.com/index.php?kw=' + urllib.parse.quote(title)
    timeout = 4
    socket.setdefaulttimeout(timeout)
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    response = urllib.request.urlopen(url=url, timeout=4, context=gcontext)
    html = response.read()
    html = BeautifulSoup(html, 'html.parser')
    info = html.find("div", class_="cont").find('ul').find('li').find('span').string
    result = re.sub("\D", "", info)
    print('获取到集数：' + result)
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
                print(title+'--更新到:',new_episode)
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


