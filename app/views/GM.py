#coding:utf-8
from flask import Blueprint, render_template

GM = Blueprint('GM', __name__)

#忘記密碼頁面
@GM.route('/forgetPassword')
def forget_Password():
   return render_template('forgotPasswordGM.html')

#輸入新密碼頁面
@GM.route('/resetPassword')
def reset_Password():
   return render_template('resetPasswordGM.html')

#登入頁面
@GM.route('/login')
def login():
   return render_template('loginGM.html')

#註冊頁面
@GM.route('/register')
def register():
   return render_template('registerGM.html')

#驗證頁面
@GM.route('/verify')
def verify(result):
    return result

#審核評論
@GM.route('/updateGrade')
def updateGrade():
    render_template('updateFrade.html')

#檢舉審核
@GM.route('/reportApprove')
def report_approve():
    render_template('reportApprove.html')