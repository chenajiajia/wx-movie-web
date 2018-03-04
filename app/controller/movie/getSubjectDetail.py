import json
import re
from flask import request
from . import movie
from ..util.dbTool import *

@movie.route('/getSubjectDetail', methods=['GET'])   #获取参数id=xxx的视频信息详情
def getSubjectDetail():
    # 获取get中的id参数，get参数为request中的args，to_dict（）将其转为字典
    args = request.args.to_dict()
    id = args.get("id")
    movieId = args.get("movieId")
    form = args.get("form")

    #检查movieId并设置返回状态码status和信息message
    status = 1
    message = "success"
    conn = mysql_conn()
    if movieId == "" or id == "":   #movieId为空
        status = 0
        message = "movieId or id is null"

    # form="sub"时说明该请求来自用户点击订阅界面的视频，此时应去除更新提醒
    if form == 'sub':
        sql = "update subscription set is_update=%s where id=%s and video_id=%s"
        param = (0, id, movieId)
        mysql_upd(conn, sql, param)

    # 连接数据库查询
    sql = "select count(*) as col from collect where id=%s and video_id=%s"
    param = (id, movieId)
    result_list = mysql_sel(conn, sql, param)
    col = result_list[0][0]
    #print(result_list)
    sql = "select count(*) as sub from subscription where id=%s and video_id=%s"
    param = (id, movieId)
    result_list = mysql_sel(conn, sql, param)
    sub = result_list[0][0]
    #print(result_list)
    sql = "select * from movie where id=%s"
    param = (movieId, )
    result_list = mysql_sel(conn, sql, param)
    mysql_close(conn)
    if len(result_list) == 0:
        status = 0
        message = "Can not find this video"

    # 查询结果转换为dictionary再转换为json传回请求者
    temp_list = []
    if status != 0:
        for row in result_list:
            result = {}
            result['movieId'] = row[0]
            result['title'] = row[1]
            result['url'] = row[2]
            result['cover'] = row[3]
            result['rating'] = row[4]
            result['director'] = row[5]
            result['composer'] = row[6]
            result['actor'] = row[7]
            result['category'] = row[8]
            result['district'] = row[9]
            result['language'] = row[10]
            matchStr = row[11].replace(' ', '').split('/')
            matchObj = re.match(r'\d{4}-\d{1,2}-\d{1,2}|\d{4}',matchStr[0],flags=0)
            result['showTime'] = matchObj.group(0)
            result['episode'] = row[12]
            result['length'] = row[13]
            result['otherName'] = row[14]
            result['description'] = row[15].replace(' ', '').replace('\t\t', '\n')
            result['imageUrls'] = row[16].decode('utf8').strip(';').split(';')
            result['col'] = int(col)
            result['sub'] = int(sub)
    temp_json = {'status': status, 'message': message, 'data': result}
    result_json = json.dumps(temp_json)

    return result_json



