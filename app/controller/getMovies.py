from flask import Flask
import json
from util.dbTool import *

app = Flask(__name__)

@app.route('/getMovies')
def getMovies():
    conn = mysql_conn()
    sql = "select * from movie limit 10"
    result_list = mysql_sel(conn, sql, '')
    print(result_list)
    conn.close
    temp_list = []
    for row in result_list:
        result = {}
        result['id'] = row[0]
        result['title'] = row[1]
        result['url'] = row[2]
        result['cover'] = row[3]
        result['rating'] = row[4]
        result['director'] = row[5]
        result['actor'] = row[6]
        result['category'] = row[7]
        result['district'] = row[8]
        result['language'] = row[9]
        result['showTime'] = row[10]
        result['episode'] = row[11]
        result['length'] = row[12]
        result['otherName'] = row[13]
        result['description'] = row[14]
        result['imageUrls'] = row[15]
        temp_list.append(result)
    result_json = json.dumps(temp_list)
    return result_json


if __name__ == '__main__':
    app.run(debug=True)

