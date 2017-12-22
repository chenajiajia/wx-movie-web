#from app import app
from flask import Flask
from app.controller.movie import movie
from app.controller.subscription import subscription
from app.controller.user import user


app = Flask(__name__)
app.register_blueprint(movie, url_prefix='/movie')
app.register_blueprint(subscription, url_prefix='/subscription')
app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)

