from flask import request
from ..util.dbTool import *
from .import user
import json


@user.route('/collect', methods=['POST'])
def collect():
    # 获取post中的参数
    #args = request.args.to_dict()
    id = request.form['id']
    movieId = request.form['movieId']
    # 检查参数并设置返回状态码status和信息message
    status = 1
    message = "success"
    if id == "" or movieId == "":
        status = 0
        message = "id or movieId is null"
    else:
        # 连接数据库插入
        conn = mysql_conn()
        sql = "insert into collect values(%s, %s)"
        param = (id, movieId)
        result = mysql_ins(conn, sql, param)
        mysql_close(conn)
        if result == 0:
            status = 0
            message = "insert into database error"

    temp_json = {"status": status, "message": message}
    result_json = json.dumps(temp_json)
    return result_json




