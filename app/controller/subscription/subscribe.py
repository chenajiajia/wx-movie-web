import json
from flask import request
from app.controller.util.getEpisode import getEp
from . import subscription
from ..util.dbTool import *


@subscription.route('/subscribe', methods=['POST'])
def subscribe():
    # 获取post中的参数
    data = request.get_data().decode('utf8')
    json_data = json.loads(data)
    id = json_data['id']
    movieId = json_data['movieId']
    episode = json_data['episode']

    # 检查参数并设置返回状态码status和信息message
    status = 1
    message = "success"
    if id == "" or movieId == "" or episode == "":
        status = 0
        message = "id or movieId or episode is null"
    else:
        conn = mysql_conn()
        sql = "select title from movie where id=%s"
        param = (movieId,)
        result = mysql_sel(conn, sql, param)
        new_episode = 0
        # 从360影视中爬取该视频最新的集数
        try:
            new_episode = getEp(result[0][0])# 获取最新集数
        except Exception as e:
            print(str(e))
            status = 0
            message = "get new episode fail"
        #连接数据库插入
        sql = "insert into subscription values(%s, %s, %s, %s, %s)"
        param = (id, movieId, 0, new_episode, episode)
        result = mysql_ins(conn, sql, param)
        mysql_close(conn)
        if result == 0:
            status = 0
            message = "insert into database error"

    temp_json = {"status": status, "message": message}
    result_json = json.dumps(temp_json)
    return result_json



