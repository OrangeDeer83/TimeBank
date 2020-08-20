#coding:utf-8
from flask import Blueprint, render_template, session, url_for, redirect
from ..models import userType

USER = Blueprint('USER', __name__)

#點數紀錄
@USER.route('/pointRecord')
def point_record():
    return "此功能未完成"
    if session.get('userType') == userType['USER']:
        return render_template('/USER/point.html')
    else:
        return redirect(url_for('USER.index'))

#忘記密碼頁面
@USER.route('/forgotPassword')
def forgot_password():
    return render_template('/USER/forgotPasswordUser.html')

#輸入新密碼頁面
@USER.route('/resetPassword/<token>')
def reset_password(token):
    return render_template('/USER/resetPasswordUser.html')

#登入頁面
@USER.route('/login')
def login():
    return redirect(url_for('USER.index'))

#註冊頁面
@USER.route('/register')
def register():
    return render_template('/USER/register.html')

#設定頁面
@USER.route('/setting')
def setting():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/setting.html')
    else:
        return redirect(url_for('USER.index'))

#點數申請
@USER.route('/application')
def application():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/application.html', userID=session.get('userID'))
    else:
        return redirect(url_for('USER.index'))

#行事曆
@USER.route('/schedule')
def schedule():
    return "此功能未完成"
    if session.get('userType') == userType['USER']:
        return render_template('/USER/schedule.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 個人介面 - 雇員評分
@USER.route('/SP/myself')
def SP_myself():
    return "此功能未完成"
    if session.get('userType') == userType['USER']:
        return render_template('/USER/myselfSP.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 個人介面 - 雇員評分
@USER.route('/SR/myself')
def SR_myself():
    return "此功能未完成"
    if session.get('userType') == userType['USER']:
        return render_template('/USER/myselfSR.html')
    else:
        return redirect(url_for('USER.index'))

#評分
@USER.route('/rating')
def rating():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/rating.html')
    else:
        return redirect(url_for('USER.index'))

#入口網站
@USER.route('/')
def index():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/homepage.html')
    else:
        return render_template('/USER/portal.html')

#承接任務頁面
@USER.route('/allTask')
def all_task():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTask.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 審核中頁面
@USER.route('/SP/allTaskChecking')
def SP_all_task_checking():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTaskSPChecking.html')
    else:
        return redirect(url_for('USER.index'))
    

#SP - 已通過頁面
@USER.route('/SP/allTaskPassed')
def SP_all_task_passed():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTaskSPPassed.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 歷史紀錄頁面
@USER.route('/SP/allTaskRecord')
def SP_all_task_record():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTaskSPRecord.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 遭拒絕頁面
@USER.route('/SP/allTaskRefused')
def SP_all_task_refused():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTaskSPRefused.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 已接受頁面
@USER.route('/SR/allTaskAccepted')
def SR_all_task_accepted():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTaskSRAccepted.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 已發布頁面
@USER.route('/SR/allTaskPassed')
def SR_all_task_passed():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTaskSRPassed.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 歷史紀錄頁面
@USER.route('/SR/allTaskRecord')
def SR_all_task_record():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/allTaskSRRecord.html')
    else:
        return redirect(url_for('USER.index'))

#新增任務
@USER.route('/createTask')
def create_task():
    if session.get('userType') == userType['USER']:
        return render_template('/USER/createTask.html')
    else:
        return redirect(url_for('USER.index'))

#個人頁面
@USER.route('/info/<userID>')
def info(userID):
    if session.get('userType') == userType['USER']:
        return render_template('/USER/myselfTask.html')
    else:
        return redirect(url_for('USER.index'))

