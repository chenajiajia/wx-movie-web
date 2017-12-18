from flask import Flask
from flask import request
from util.dbTool import *
import json

app = Flask(__name__)

@app.route('/collect', methods=['GET'])
def collect():
    # 获取get中的参数，get参数为request中的args，to_dict（）将其转为字典
    args = request.args.to_dict()
    id = args.get("id", "")
    movieId = args.get("movieId", "")
    episode = args.get("episode", "")

    # 检查参数并设置返回状态码status和信息message
    status = 1
    message = "success"
    if id == "" or movieId == "" or episode == "":
        status = 0
        message = "id or movieId or episode is null"
    else:
        # 连接数据库插入
        conn = mysql_conn()
        sql = "insert into collect values(%s, %s, %s, %s, %s)"
        param = (id, movieId, 0, 18, episode)
        result = mysql_ins(conn, sql, param)
        mysql_close(conn)
        if result == 0:
            status = 0
            message = "insert into database error"

    temp_json = {"status": status, "message": message}
    result_json = json.dumps(temp_json)
    return result_json


if __name__ == '__main__':
    app.run(debug=True)

