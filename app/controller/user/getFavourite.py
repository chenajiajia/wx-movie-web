from flask import request
from ..util.dbTool import *
from . import user
import json


@user.route('/getFavourite', methods=['POST'])
def getFavourite():
    # 获取post中的参数
    data = request.get_data().decode('utf8')
    json_data = json.loads(data)
    id = json_data['id']

    # 检查参数并设置返回状态码status和信息message
    status = 1
    message = "success"
    if id == "":
        status = 0
        message = "id is null"
    else:
        # 连接数据库查询
        conn = mysql_conn()
        sql = "select tag from favourite where id = %s"
        param = (id, )
        result = mysql_sel(conn, sql, param)
        mysql_close(conn)

    temp_json = {"status": status, "message": message, "data":result[0][0]}
    result_json = json.dumps(temp_json)
    return result_json



