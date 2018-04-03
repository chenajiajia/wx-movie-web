from flask import request
from ..util.dbTool import *
from . import movie
from ..util.recommend import *
import json


@movie.route('/getRecommend', methods=['GET'])
def getRecommend():
    id = request.values.get("id")
    start = request.args.get("start", 0)
    #由用户填写的数据推荐视频
    conn = mysql_conn()
    param = (id,)
    sql = "select tag from favourite where id=%s"
    result_list = mysql_sel(conn, sql, param)
    if result_list:
        district = '中国'
        category = '剧情'
        favourite = json.loads(result_list[0][0].replace('\'', '\"'))
        if len(favourite['locate']):
            district = favourite['locate'][0]
        if len(favourite['category']):
            category = favourite['category'][0]
    else:
        district =  '中国'
        category =  '剧情'
    temp_list = []
    sql = "select id,title,cover,rating,director,actor,category from movie where district like %s and category like %s limit %s, 10"
    param = ('%'+district+'%','%'+category+'%',int(start))
    result_list = mysql_sel(conn, sql, param)

    if len(result_list) == 0:
        status = 1
        message = "Can not find more video"
    for row in result_list:
        result = {}
        result['movieId'] = row[0]
        result['title'] = row[1]
        result['cover'] = row[2]
        result['rating'] = row[3]
        result['director'] = row[4]
        result['actor'] = row[5]
        result['category'] = row[6]

        temp_list.append(result)

    #从数据库中取出用户物品列表
    param = ()
    sql = "select user_id, video_id, weight from userItem"
    result_list = mysql_sel(conn, sql,param)
    #mysql_close(conn)
    if len(result_list) == 0:
        status = 1
        message = "No userItem"

    #将用户物品列表数组转为dict
    userItem = dict()
    item = dict()
    for row in result_list:
        if row[0] in userItem:
            userItem[row[0]].update({row[1]: row[2]})
        else:
            userItem.update({row[0]: {row[1]: row[2]}})

    #判断用户物品列表中是否存在当前用户
    if id in userItem:
        #计算出物品间相似度
        Similarity = ItemSimilarity(userItem)
        #得到与用户感兴趣物品最相似的前N个物品
        recommendList = Recommendation(userItem, id, Similarity, 10)
        #对结果按感兴趣程度排序
        rankList = sorted(recommendList.items(), key=lambda s: s[1], reverse=True)

        #通过rankList中的id查询影片信息
        status = 1
        message = ''

        for movieId,weight in rankList:
            sql = "select id,title,cover,rating,director,actor,category from movie where id=%s"
            param = (movieId,)
            result_list = mysql_sel(conn, sql, param)

            if len(result_list) == 0:
                status = 1
                message = "Can not find more video"
            for row in result_list:
                result = {}
                result['movieId'] = row[0]
                result['title'] = row[1]
                result['cover'] = row[2]
                result['rating'] = row[3]
                result['director'] = row[4]
                result['actor'] = row[5]
                result['category'] = row[6]

                temp_list.append(result)

    mysql_close(conn)
    temp_json = {'status': status, 'message': message, 'data': temp_list}
    result_json = json.dumps(temp_json)

    return result_json
