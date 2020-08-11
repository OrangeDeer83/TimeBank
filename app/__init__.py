#coding:utf-8
from flask import Flask
from flask_cors import CORS
from .models import db


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
CORS(app)
db.init_app(app)

#匯入views
from .views.USER_module import USER
from .views.account import Account
from .views.apply import Apply
from .views.calender import Calender
from .views.comment import Comment
from .views.HRManage import HRManage
from .views.point import Point
from .views.portal import Portal
from .views.profile import Profile
from .views.report import Report
from .views.task import Task
from .views.test import test

#註冊blueprint設定路徑
app.register_blueprint(USER, url_prefix='/USER')
app.register_blueprint(Account, url_prefix='/account')
app.register_blueprint(Apply, url_prefix='/apply')
app.register_blueprint(Calender, url_prefix='/calender')
app.register_blueprint(Comment, url_prefix='/comment')
app.register_blueprint(HRManage, url_prefix='/HRManage')
app.register_blueprint(Point, url_prefix='/point')
app.register_blueprint(Portal, url_prefix='/portal')
app.register_blueprint(Profile, url_prefix='/profile')
app.register_blueprint(Report, url_prefix='/report')
app.register_blueprint(Task, url_prefix='/task')
app.register_blueprint(test, url_prefix='/test')