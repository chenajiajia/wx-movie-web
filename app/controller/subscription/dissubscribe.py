from flask import request
from ..util.dbTool import *
from .import subscription
import json


@subscription.route('/dissubscribe', methods=['POST'])
def dissubscribe():
    # 获取post中的参数
    data = request.get_data().decode('utf8')
    json_data = json.loads(data)
    id = json_data['id']
    movieId = json_data['movieId']
    # 检查参数并设置返回状态码status和信息message
    status = 1
    message = "success"
    if id == "" or movieId == "":
        status = 0
        message = "id or movieId is null"
    else:
        # 连接数据库插入
        conn = mysql_conn()
        sql = "delete from subscription where id=%s and video_id=%s"
        param = (id, movieId)
        result = mysql_del(conn, sql, param)
        mysql_close(conn)
        if result == 0:
            status = 0
            message = "delete error"

    temp_json = {"status": status, "message": message}
    result_json = json.dumps(temp_json)
    return result_json




