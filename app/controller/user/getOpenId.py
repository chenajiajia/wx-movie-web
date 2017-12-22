from flask import request
from urllib import request as urlRequest
from ..util.dbTool import *
from . import user
import json


@user.route('/getOpenId')
def getOpenId():
    jscode = request.values.get('code')
    APPID = 'wxa4123ad325278cdf'
    SECRET = '125a6cbbd99f928c6b0d98406842560c'
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + APPID + '&secret=' + SECRET + '&js_code='\
        + jscode + '&grant_type=authorization_code'


    response = urlRequest.urlopen(url) 
    page = response.read()
    page = json.loads(page.decode('utf-8'))
    print(page)
    res = dict()
    res['status'] = 1
    res['data'] = page
    return json.dumps(res)


@user.route('/login')
def login():
    id = request.values.get("id")
    name = request.values.get("nickName")
    sex = request.values.get("gender")
    address = request.values.get("city")
    img_url = request.values.get("avatarUrl")

    
    conn = mysql_conn()
    data = (id, name, sex, address, img_url)
    #查询用户是否存在
    sql_select = "select * from user where id=%s"
    where = (id, )
    status = mysql_sel(conn, sql_select, where)
    if not status:
        # 记录用户信息
        sql_insert = "insert into user (id, name, sex, address, img_url) values( %s, %s, %s, %s, %s)"
        
        status = mysql_ins(conn, sql_insert, data)
    res = dict()
    res['status'] = status
    res['data'] = data
    
    return json.dumps(res)


