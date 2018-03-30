# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from logging.handlers import RotatingFileHandler
import logging

db_cmdb = SQLAlchemy()
db_zeus = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = u"请登录!"


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config['pre-release'])
    config['pre-release'].init_app(app)

    db_cmdb.init_app(app)
    db_zeus.init_app(app)
    login_manager.init_app(app)

    logpath = app.config['LOGPATH']
    handler = RotatingFileHandler(logpath, mode='w', maxBytes=10 * 1024 * 1024, backupCount=20, encoding='UTF-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    from .cmdb import cmdb, cmdb_api
    from .auth import auth
    from .ad import ad
    from .views import views
    from .statistics import statistics
    from .zeus import zeus

    app.register_blueprint(cmdb, url_prefix='/cmdb')
    app.register_blueprint(cmdb_api, url_prefix='/cmdb/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(ad, url_prefix='/ad')
    app.register_blueprint(zeus, url_prefix='/zeus')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(statistics, url_prefix='/statistics')

    return app
