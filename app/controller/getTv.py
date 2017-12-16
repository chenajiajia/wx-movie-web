from flask import Flask
from flask import request
from util.dbTool import *
import json

app = Flask(__name__)

@app.route('/getTv', methods=['GET'])   #获取参数limit后的十条电视剧信息
def getTv():
    # 获取get中的start参数，get参数为request中的args，to_dict（）将其转为字典
    args = request.args.to_dict()
    start = args.get("start", "0")

    # 检查start并设置返回状态码status和信息message
    status = 1
    message = "success"
    if start == "":  # start为空
        status = 0
        message = "start is null"

    # 查询结果为list，转换为dictionary再转换为json传回请求者
    temp_list = []
    if status != 0:
        # 连接数据库查询
        conn = mysql_conn()
        sql = "select id,title,cover,rating,director,actor,category from movie where episode!=%s limit %s,%s"
        param = ('0', int(start), 10)
        result_list = mysql_sel(conn, sql, param)
        mysql_close(conn)
        if len(result_list) == 0:
            status = 0
            message = "Can not find more video"
        for row in result_list:
            result = {}
            result['id'] = row[0]
            result['title'] = row[1]
            #result['url'] = row[2]
            result['cover'] = row[2]
            result['rating'] = row[3]
            result['director'] = row[4]
            #result['composer'] = row[6]
            result['actor'] = row[5]
            result['category'] = row[6]
            #result['district'] = row[9]
            #result['language'] = row[10]
            #result['showTime'] = row[11]
            #result['episode'] = row[12]
            #result['length'] = row[13]
            #result['otherName'] = row[14]
            #result['description'] = row[15].replace(' ', '').replace('\t\t', '\n')
            #result['imageUrls'] = row[16].decode('utf8').strip(';').split(';')
            temp_list.append(result)
    temp_json = {'status': status, 'message': message, 'data': temp_list}
    result_json = json.dumps(temp_json)

    return result_json


if __name__ == '__main__':
    app.run(debug=True)

