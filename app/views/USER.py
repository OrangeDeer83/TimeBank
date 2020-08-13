#coding:utf-8
from flask import Blueprint, render_template, session, url_for, redirect

USER = Blueprint('USER', __name__)

#點數紀錄
@USER.route('/record')
def record():
    return render_template('point.html')

#忘記密碼頁面
@USER.route('/forgotPassword/<token>')
def forgotPassword(token):
    return render_template('forgotPasswordUser.html')

#輸入新密碼頁面
@USER.route('/resetPassword')
def resetPassword():
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
    return render_template('setting.html')

#點數申請
@USER.route('/application')
def application():
    return render_template('application.html')

#行事曆
@USER.route('/schedule')
def schedule():
    return render_template('schedule.html')

#SP - 個人介面 - 雇員評分
@USER.route('/SP/myself')
def SP_mysel():
    return render_template('myselfSP.html')

#SR - 個人介面 - 雇員評分
@USER.route('/SR/myself')
def SR_mysel():
    return render_template('myselfSR.html')

#評分
@USER.route('/rating')
def rating():
    return render_template('rating.html')

#入口網站
@USER.route('/')
def index():
    if session.get('userType') == 1:
        return render_template('hom.html')
    else:
        return render_template('portal.html')

#承接任務頁面
@USER.route('/allTask')
def all_task():
    return render_template('allUSER.html')

#SP - 審核中頁面
@USER.route('/SP/allTaskChecking')
def SP_all_taskchecking():
    return render_template('allTaskSPChecking.html')

#SP - 已通過頁面
@USER.route('/SP/allTaskPassed')
def SP_all_task_passed():
    return render_template('allTaskSPPassed.html')

#SP - 歷史紀錄頁面
@USER.route('/SP/allTaskRecord')
def SP_all_task_record():
    return render_template('allTaskSPRecord.html')

#SP - 遭拒絕頁面
@USER.route('/SP/allTaskRefused')
def SP_all_task_refused():
    return render_template('allTaskSPRefused.html')

#SR - 已接受頁面
@USER.route('/SR/allTaskAccepted')
def SR_all_task_accepted():
    return render_template('allTaskSPAccepted.html')

#SR - 已發布頁面
@USER.route('/SR/allTaskPassed')
def SR_all_task_passed():
    return render_template('allTaskSRPassed.html')

#SR - 歷史紀錄頁面
@USER.route('/SR/allTaskRecord')
def SR_all_task_record():
    return render_template('allTaskSRRecord.html')

#新增任務
@USER.route('/createTask')
def create_task():
    return render_template('createUSER.html')

#個人頁面 - 已發任務
@USER.route('/myselfTask')
def myself_task():
    return render_template('myselfTask.html')