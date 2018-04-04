import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import socket
from flask import request
from . import movie
from retrying import retry
import json
import ssl

#判断是否是异常
def retry_if_urllib_error(exception):
    # if isinstance(exception, AttributeError):
    #     return False
    return isinstance(exception, Exception)

# 当发生异常时会重试获取集数，重试次数stop_max_attempt_number为5
@retry(retry_on_exception = retry_if_urllib_error, stop_max_attempt_number = 5)
@movie.route('/getURL', methods=['GET'])
def getURL():
    # 获取get中的title参数，get参数为request中的args，to_dict（）将其转为字典
    args = request.args.to_dict()
    title = args.get("title", "0")
    episode = int(args.get("episode", "0"))

    # 检查start并设置返回状态码status和信息message
    status = 1
    message = "success"
    if title == "":  # start为空
        status = 0
        message = "title is null"

    url = 'https://so.360kan.com/index.php?kw=' + urllib.parse.quote(title)
    timeout = 4
    socket.setdefaulttimeout(timeout)
    info = ''
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib.request.urlopen(url=url, timeout=4, context=gcontext)
        html = response.read()
        html = BeautifulSoup(html, 'html.parser')
        if episode!=0:
            info = html.find("div", class_="b-series-number-container g-clear"
                                           "").find('a')['href']
        else:
            info = html.find("div", class_="button-container g-clear"
                                           "").find('a')['href']
    except Exception as e:
        print(str(e))
        status = 2
        message = "no url"
        info = ''
    temp = {}
    temp['url'] = info
    temp_json = {'status': status, 'message': message, 'data': temp}
    print(temp_json)
    result_json = json.dumps(temp_json)

    return result_json

# if __name__ == '__main__':
#     while True:
#         getURL('A频道')


