from flask import Flask
from flask import request
from ..util.dbTool import *
from . import movie
import json

@movie.route('/search', methods=['GET'])   #获取参数id=xxx的视频信息详情
def search():
    # 获取get中的search内容wd参数，get参数为request中的args，to_dict（）将其转为字典
    args = request.args.to_dict()
    wd = args.get("wd")


    #检查wd并设置返回状态码status和信息message
    status = 1
    message = "success"
    if wd == "":   #wd为空
        status = 0
        message = "wd is null"

    # 连接数据库查询
    conn = mysql_conn()
    sql = "select *,(length(title)-length(%s)) as rn from movie where title " \
          "like %s order by rn limit 30"
    param = (wd, '%'+wd+'%')
    result_list = mysql_sel(conn, sql, param)
    mysql_close(conn)
    if len(result_list) == 0:
        status = 0
        message = "Can not find this video"
    # print(result_list)
    # 查询结果转换为dictionary再转换为json传回请求者
    temp_list = []
    if status != 0:
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
            result['showTime'] = row[11]
            # result['episode'] = row[12]
            # result['length'] = row[13]
            # result['otherName'] = row[14]
            # result['description'] = row[15].replace(' ', '').replace('\t\t', '\n')
            # result['imageUrls'] = row[16].decode('utf8').strip(';').split(';')
            temp_list.append(result)
    temp_json = {'status': status, 'message': message, 'data': temp_list}
    result_json = json.dumps(temp_json)

    return result_json



