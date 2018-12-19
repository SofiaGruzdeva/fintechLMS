from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import app_config
from .models import db

from .views.user_view import user_api as user_blueprint
from .views.study_group_view import study_group_api as study_group_blueprint
from .views.study_course_view import study_course_api as study_course_blueprint


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(study_group_blueprint, url_prefix='/study_group')
    app.register_blueprint(study_course_blueprint, url_prefix='/study_course')

    @app.route('/', methods=['GET'])
    def index():

        return 'Congratulations!'

    return app
