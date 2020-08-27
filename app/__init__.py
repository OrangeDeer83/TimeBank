#coding:utf-8
from flask import Flask
from flask_cors import CORS
from .models import db


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
CORS(app)
db.init_app(app)

#匯入controllers
from .controllers.account import Account
from .controllers.allotment import Allotment
from .controllers.apply import Apply
from .controllers.calendar import Calendar
from .controllers.comment import Comment
from .controllers.HRManage import HRManage
from .controllers.notice import Notice
from .controllers.point import Point
from .controllers.portal import Portal
from .controllers.profile import Profile
from .controllers.report import Report
from .controllers.task import Task
from .controllers.test import test

#匯入views
from .views.Admin import Admin
from .views.GM import GM
from .views.USER import USER

#註冊blueprint設定路徑
app.register_blueprint(Account, url_prefix='/account')
app.register_blueprint(Admin, url_prefix='/Admin')
app.register_blueprint(Allotment, url_prefix='/allotment')
app.register_blueprint(Apply, url_prefix='/apply')
app.register_blueprint(Calendar, url_prefix='/calendar')
app.register_blueprint(Comment, url_prefix='/comment')
app.register_blueprint(GM, url_prefix='/GM')
app.register_blueprint(HRManage, url_prefix='/HRManage')
app.register_blueprint(Notice, url_prefix='/notice')
app.register_blueprint(Point, url_prefix='/point')
app.register_blueprint(Portal, url_prefix='/portal')
app.register_blueprint(Profile, url_prefix='/profile')
app.register_blueprint(Report, url_prefix='/report')
app.register_blueprint(Task, url_prefix='/task')
app.register_blueprint(test, url_prefix='/test')
app.register_blueprint(USER, url_prefix='/USER')