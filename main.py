from flask import Flask, jsonify, abort, make_response, request
from flask.json import JSONEncoder
from flask_cors import CORS

from datetime import datetime

from api.users import User, users_api
from api.consumptions import Consumption, consumptions_api, FORMATO_DATE
from api.buildings import Building, buildings_api

app = Flask(__name__, static_url_path="")
CORS(app)

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id': obj.id,
                'email': obj.email,
                'password': obj.password,
                'logged': obj.logged
                }
        if isinstance(obj, Consumption):
            return {
                'date': datetime.strftime(obj.date, FORMATO_DATE),
                'value': obj.value
            }
        if isinstance(obj, Building):
            return {
                'id': obj.id,
                'name': obj.name
                # 'consumptions': obj.consumptions
            }
                
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

app.register_blueprint(users_api)
app.register_blueprint(consumptions_api)
app.register_blueprint(buildings_api)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/index.html')
def indexhtml():
    return app.send_static_file('index.html')

@app.route('/buildings.html')
def buildings():
    return app.send_static_file('buildings.html')

if __name__ == '__main__':
    app.run(port='2000', debug=True)
    