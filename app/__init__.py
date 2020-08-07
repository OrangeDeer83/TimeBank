#coding:utf-8
from flask import Flask
from .models import db


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
db.init_app(app)

#匯入views
from .views.USER_module import USER
from .views.account import account
from .views.apply import apply
from .views.calender import calender
from .views.comment import comment
from .views.HRManage import HRManage
from .views.point import point
from .views.portal import portal
from .views.profile import profile
from .views.report import report
from .views.task import task
from .views.test import test

#註冊blueprint設定路徑
app.register_blueprint(USER, url_prefix='/USER')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(apply, url_prefix='/apply')
app.register_blueprint(calender, url_prefix='/calender')
app.register_blueprint(comment, url_prefix='/comment')
app.register_blueprint(HRManage, url_prefix='/HRManage')
app.register_blueprint(point, url_prefix='/point')
app.register_blueprint(portal, url_prefix='/portal')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(task, url_prefix='/task')
app.register_blueprint(test, url_prefix='/test')