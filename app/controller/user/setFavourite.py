from flask import request
from ..util.dbTool import *
from . import user
import json


@user.route('/setFavourite', methods=['POST'])
def setFavourite():
    # 获取post中的参数
    data = request.get_data().decode('utf8')
    json_data = json.loads(data)
    id = json_data['id']
    # category = json_data['category']
    # district = json_data['district']
    # decade = json_data['decade']
    del json_data['id']
    #print(json_data)

    # 检查参数并设置返回状态码status和信息message
    status = 1
    message = "success"
    if id == "":
        status = 0
        message = "id is null"
    else:
        # 连接数据库查询是否有存在记录
        print (json_data)
        conn = mysql_conn()
        sql = "select count(*) from favourite where id = %s"
        param = (id, )
        result = mysql_sel(conn, sql, param)
        if result[0][0] != 0:
            # 连接数据库更新
            sql = "update favourite set tag = %s where id = %s"
            param = (str(json_data), id)
            result = mysql_upd(conn, sql, param)
            mysql_close(conn)
            if result == 0:
                status = 0
                message = "update database error"
        else :
        # 连接数据库插入

            sql = "insert into favourite values(%s, %s)"
            param = (id, str(json_data))
            result = mysql_ins(conn, sql, param)
            mysql_close(conn)
            if result == 0:
                status = 0
                message = "insert into database error"

    temp_json = {"status": status, "message": message}
    result_json = json.dumps(temp_json)
    return result_json



