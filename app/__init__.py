from flask import Flask
from flask import Blueprint
from flask_restful import Api
from .routes import web_routes, api_routes
from .environment import env
from .extensions import db, bcrypt

web_blueprint = Blueprint(
    'app', __name__, template_folder='templates', static_folder='static', url_prefix='/')
web_routes(web_blueprint)
api_blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(api_blueprint, catch_all_404s=True)
api_routes(api)


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(env[env_name])
    db.init_app(app)
    bcrypt.init_app(app)
    return app
