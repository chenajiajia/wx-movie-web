from flask import Flask
from flask import request
from util.dbTool import *
import json

app = Flask(__name__)

@app.route('/getMovies', methods=['GET'])   #获取参数limit后的十条电影信息
def getMovies():
    #获取get中的limit参数，get参数为request中的args，to_dict（）将其转为字典
    args = request.args.to_dict()
    start = args.get("limit","0")
    #连接数据库查询
    conn = mysql_conn()
    sql = "select * from movie where episode=%s limit %s,%s"
    param = ('0', int(start), 10)
    result_list = mysql_sel(conn, sql, param)
    mysql_close(conn)
    #查询结果为list，转换为dictionary再转换为json传回请求者
    temp_list = []
    for row in result_list:
        result = {}
        result['id'] = row[0]
        result['title'] = row[1]
        # result['url'] = row[2]
        result['cover'] = row[3]
        result['rating'] = row[4]
        result['director'] = row[5]
        # result['composer'] = row[6]
        result['actor'] = row[7]
        result['category'] = row[8]
        # result['district'] = row[9]
        # result['language'] = row[10]
        # result['showTime'] = row[11]
        # result['episode'] = row[12]
        # result['length'] = row[13]
        # result['otherName'] = row[14]
        # result['description'] = row[15].replace(' ', '').replace('\t\t', '\n')
        # result['imageUrls'] = row[16].decode('utf8').strip(';').split(';')
        temp_list.append(result)
    result_json = json.dumps(temp_list)
    return result_json


if __name__ == '__main__':
    app.run(debug=True)

