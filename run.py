#from app import app
from flask import Flask
from app.controller.movie import movie
from app.controller.subscription import subscription
from app.controller.user import user
from flask import request
import time
from app.controller.util.dbTool import *
import json

app = Flask(__name__)
app.register_blueprint(movie, url_prefix='/movie')
app.register_blueprint(subscription, url_prefix='/subscription')
app.register_blueprint(user, url_prefix='/user')


@app.before_request
def before_request():
    url = request.path
    if request.method == 'POST' :
        data = request.get_data().decode('utf8')
        json_data = json.loads(data)
        id = json_data['id']
        if 'getSubjectDetail' in url or 'collect' in url or 'subscribe' in url:
            movieId = json_data['movieId']
    else:
        id = request.args.get('id')
        movieId = request.args.get("movieId")
    timestamp = time.time()

    print(url)
    #根据客户端请求的url判断用户行为，记录日志，更新用户物品表
    if 'getSubjectDetail' in url :
        behaviour = '点击'
        weight = 1
    elif 'collect' in url :
        behaviour = '收藏'
        weight = 2
    elif 'subscribe' in url:
        behaviour = '订阅'
        weight = 3
    else :
        return
        # 连接数据库插入click,记录用户行为日志
    conn = mysql_conn()
    sql = "insert into click(user_id, behaviour, weight, video_id, timestamp) values(%s, %s, %s, %s, %s)"
    param = (id, behaviour, weight, movieId, timestamp)
    result = mysql_ins(conn, sql, param)
    #mysql_close(conn)
    if result == 0:
        status = 0
        message = "insert into database error"

    # 更新useritem
    sql = "select id,weight from userItem where user_id=%s and video_id=%s"
    param = (id, movieId)
    result_list = mysql_sel(conn, sql, param)
    #mysql_close(conn)
    if len(result_list) == 0:
        #conn = mysql_conn()
        sql = "insert into userItem(user_id, weight, video_id) values(%s, %s, %s)"
        param = (id, weight, movieId)
        result = mysql_ins(conn, sql, param)
        #mysql_close(conn)
        if result == 0:
            status = 0
            message = "insert into database error"
    else:
        id = result_list[0][0]
        weight = result_list[0][1] + weight
        sql = "update userItem set weight = %s where id = %s"
        param = (weight, id)
        result = mysql_upd(conn, sql, param)
        if result == 0:
            status = 0
            message = "update database error"

if __name__ == '__main__':
    app.run(debug=True)

