from flask import Flask
from flask import request
import json
from util.dbTool import *
app = Flask(__name__)


@app.route('/login')
def login():
	 
	# id = request.values.get("id")
 #    username = request.values.get("name") 
 #    sex = request.values.get("sex")
 #    address = request.values.get("address")

    #记录用户信息
    conn=mysql_conn()
    res=dict()
    res['status']=1
    return json.dumps(res)

if __name__ == '__main__':
    app.run(debug=True)

