from flask import Flask
from flask import request
from app.controller.util.dbTool import *
from . import subscription
import json


@subscription.route('/getSubscription', methods=['POST'])
def getSubscription():
    # 获取post中的参数
    id = request.form['id']
    #args = request.args.to_dict()
    #id = args.get("id", "")
    #movieId = args.get("movieId", "")
    #episode = args.get("episode", "")

    # 检查参数并设置返回状态码status和信息message
    status = 1
    message = "success"
    temp_list = []
    if id == "":
        status = 0
        message = "id is null"
    else:
        # 连接数据库查询
        conn = mysql_conn()
        sql = "select movie.id,title,cover,update_episode from movie,subscription where subscription.id=%s and video_id=movie.id"
        param = (id, )
        result_list = mysql_sel(conn, sql, param)
        mysql_close(conn)
        if len(result_list)==0:
            status = 1
            message = "No subscriptions"
        for row in result_list:
            result = {}
            result['movieId'] = row[0]
            result['title'] = row[1]
            result['cover'] = row[2]
            result['update_episode'] = row[3]
            temp_list.append(result)

    temp_json = {"status": status, "message": message, "data": temp_list}
    result_json = json.dumps(temp_json)
    return result_json



