import urllib.request, urllib.error, urllib.parse
import requests
from bs4 import BeautifulSoup
import re
import time
import socket
from retrying import retry


# headers = {}
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                         'Chrome/64.0.3282.168 Safari/537.36',
#            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#            'Accept-Language':'zh-CN,zh;q=0.9',
#            'Connection':'close'}

url = 'https://so.360kan.com/index.php?kw=' + urllib.parse.quote("寻秦记")

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

def retry_if_urllib_error(exception):
    return isinstance(exception, Exception)

@retry(retry_on_exception=retry_if_urllib_error, stop_max_attempt_number=5)
def retryTest(url):
    timeout = 4
    socket.setdefaulttimeout(timeout)
    response = urllib.request.urlopen(url=url, timeout=4)
    html = response.read()
    html = BeautifulSoup(html, 'html.parser')
    info = html.find("div", class_="cont").find('ul').find('li').find('span').string
    result = re.sub("\D", "", info)
    print(result)
    # raise urllib.error.URLError('info')
    # raise urllib.error.HTTPError('info')
    # raise socket.timeout('info')

if __name__ == '__main__':
    while (1):
        start = time.clock()
        retryTest(url)
        print('over')
        # try:
        #     # request = urllib.request.Request(url=url, headers=headers)
        #
        # except urllib.error.URLError as e:
        #     print(str(e))
        # except urllib.error.HTTPError as e:
        #     print(str(e))
        # except socket.timeout as e:
        #     print(str(e))
        end = time.clock()
        print("Running time: %s Seconds" % (end - start))
        time.sleep(3)


