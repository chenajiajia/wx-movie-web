from flask import Flask
from flask import request
import util.dbTool
app = Flask(__name__)


@app.route('/login')
def login():
	pass
	# id = request.values.get("id")
 #    username = request.values.get("name") 
 #    sex = request.values.get("sex")
 #    address = request.values.get("address")

    #记录用户信息
    #conn=mysql_conn()

if __name__ == '__main__':
    app.run(debug=True)

