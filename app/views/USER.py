#coding:utf-8
from flask import Blueprint, render_template, session, url_for, redirect
from ..models import userType

USER = Blueprint('USER', __name__)

#點數紀錄
@USER.route('/pointRecord')
def record():
    if session['userType'] != userType['USER']:
        return render_template('point.html')
    else:
        return redirect(url_for('USER.index'))

#忘記密碼頁面
@USER.route('/forgotPassword')
def forgotPassword():
    return render_template('forgotPasswordUser.html')

#輸入新密碼頁面
@USER.route('/resetPassword/<token>')
def resetPassword(token):
    return render_template('resetPasswordUser.html')

#登入頁面
@USER.route('/login')
def login():
    return redirect(url_for('USER.index'))

#註冊頁面
@USER.route('/register')
def register():
    return render_template('register.html')

#設定頁面
@USER.route('/setting')
def setting():
    if session['userType'] != userType['USER']:
        return render_template('setting.html')
    else:
        return redirect(url_for('USER.index'))

#點數申請
@USER.route('/application')
def application():
    if session['userType'] != userType['USER']:
        return render_template('application.html')
    else:
        return redirect(url_for('USER.index'))

#行事曆
@USER.route('/schedule')
def schedule():
    if session['userType'] != userType['USER']:
        return render_template('schedule.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 個人介面 - 雇員評分
@USER.route('/SP/myself')
def SP_mysel():
    if session['userType'] != userType['USER']:
        return render_template('myselfSP.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 個人介面 - 雇員評分
@USER.route('/SR/myself')
def SR_mysel():
    if session['userType'] != userType['USER']:
        return render_template('myselfSR.html')
    else:
        return redirect(url_for('USER.index'))

#評分
@USER.route('/rating')
def rating():
    if session['userType'] != userType['USER']:
        return render_template('rating.html')
    else:
        return redirect(url_for('USER.index'))

#入口網站
@USER.route('/')
def index():
    if session['userType'] == userType['USER']:
        return render_template('homepage.html')
    else:
        return render_template('portal.html')

#承接任務頁面
@USER.route('/allTask')
def all_task():
    if session['userType'] != userType['USER']:
        return render_template('allUSER.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 審核中頁面
@USER.route('/SP/allTaskChecking')
def SP_all_taskchecking():
    if session['userType'] != userType['USER']:
        return render_template('allTaskSPChecking.html')
    else:
        return redirect(url_for('USER.index'))
    

#SP - 已通過頁面
@USER.route('/SP/allTaskPassed')
def SP_all_task_passed():
    if session['userType'] != userType['USER']:
        return render_template('allTaskSPPassed.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 歷史紀錄頁面
@USER.route('/SP/allTaskRecord')
def SP_all_task_record():
    if session['userType'] != userType['USER']:
        return render_template('allTaskSPRecord.html')
    else:
        return redirect(url_for('USER.index'))

#SP - 遭拒絕頁面
@USER.route('/SP/allTaskRefused')
def SP_all_task_refused():
    if session['userType'] != userType['USER']:
        return render_template('allTaskSPRefused.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 已接受頁面
@USER.route('/SR/allTaskAccepted')
def SR_all_task_accepted():
    if session['userType'] != userType['USER']:
        return render_template('allTaskSPAccepted.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 已發布頁面
@USER.route('/SR/allTaskPassed')
def SR_all_task_passed():
    if session['userType'] != userType['USER']:
        return render_template('allTaskSRPassed.html')
    else:
        return redirect(url_for('USER.index'))

#SR - 歷史紀錄頁面
@USER.route('/SR/allTaskRecord')
def SR_all_task_record():
    if session['userType'] != userType['USER']:
        return render_template('allTaskSRRecord.html')
    else:
        return redirect(url_for('USER.index'))

#新增任務
@USER.route('/createTask')
def create_task():
    if session['userType'] != userType['USER']:
        return render_template('createUSER.html')
    else:
        return redirect(url_for('USER.index'))

#個人頁面 - 已發任務
@USER.route('/info/<userID>')
def info(userID):
    if session['userType'] != userType['USER']:
        return render_template('myselfTask.html')
    else:
        return redirect(url_for('USER.index'))