import os
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from application import config
from application.config import Config
from application.database import db

app = None
api = None

custom_errors = {
    'NotFoundError': {
        'message': "A user with that username already exists.",
        'status': 400,
    }
}

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
    if os.getenv('ENV', "development") == "production":
        raise Exception("This setup is not for production use")
    else:
        print("Starting Local Development")
        app.config.from_object(Config)
    db.init_app(app)
    api = Api(app, errors=custom_errors)
    cors = CORS(app)
    app.app_context().push()
    return app, api ,cors

app, api, cors= create_app()

from application.controllers import *
from application.api import *
api.add_resource(UserAPI, "/api/user/<string:user_name>")
api.add_resource(ListAPI, "/api/user/<string:user_name>/list", "/api/user/<string:user_name>/list/<string:list_name>")
api.add_resource(CardAPI, "/api/user/<string:user_name>/list/<string:list_name>/card" ,"/api/user/<string:user_name>/list/<string:list_name>/card/<string:title>")
api.add_resource(MoveCardAPI,"/api/user/<string:user_name>/list/<string:list_name>/card/<string:title>/move")
api.add_resource(MoveListAPI, "/api/user/<string:user_name>/list/<string:list_name>/move_all")

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)