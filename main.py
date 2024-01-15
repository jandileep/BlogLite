import os
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_restful import Resource, Api,fields,marshal_with
from flask import make_response
from flask_restful import reqparse 
from werkzeug .exceptions import HTTPException

app = None
class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response('',status_code)
class BuisnessValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message = {'error_code':error_code,'error_message':error_message}
        self.response = make_response(json.dumps(message),status_code)
def create_app():
    
    app = Flask(__name__)
    if os.getenv("ENV","development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
api = Api(app)

from application.login_controllers import *
from application.post_controllers import *
from application.profile_controllers import *
from application.blog_controllers import *
from application.API_files import *
api.add_resource(SignupAPI,"/api/signup/<user_name>", "/api/signup")
api.add_resource(PostAPI,"/api/post/<user_name>","/api/<user_name>/post/<post_id>")
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)