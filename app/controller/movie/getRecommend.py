from flask import request
from ..util.dbTool import *
from . import movie
from ..util.recommend import *
import json


@movie.route('/getRecommend', methods=['GET'])
def getRecommend():
    conn = mysql_conn()
    sql = "select * from userItem"
    result_list = mysql_sel(conn, sql)
    mysql_close(conn)
    if len(result_list) == 0:
        status = 1
        message = "No collect"
    for row in result_list:
        userItem = []
        item = []
        result = {}
        item[row[1]] = row[2]
        result.append(item)
        userItem[row[0]] =result

    Similarity = ItemSimilarity(userItem)
