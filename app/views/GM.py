#coding:utf-8
from flask import Blueprint, render_template, session, redirect, url_for
from ..models import userType

GM = Blueprint('GM', __name__)

#忘記密碼頁面
@GM.route('/forgotPassword')
def forgot_password():
   return render_template('forgotPasswordGM.html')

#輸入新密碼頁面
@GM.route('/resetPasswor/<token>')
def reset_password(token):
   return render_template('resetPasswordGM.html')

#登入頁面
@GM.route('/login')
def login():
   if session.get('userType') == userType['GM']:
      return redirect(url_for('GM.update_grade'))
   else:
      return render_template('loginGM.html')

#註冊頁面
@GM.route('/register')
def register():
   return render_template('registerGM.html')

#驗證頁面
@GM.route('/verify/<result>')
def verify(result):
   if result == '1':
      return '資料庫錯誤，請稍後再試'
   elif result == '2':
      return '資料庫錯誤，請稍後再試'
   elif result == '3':
      return '帳號驗證成功，等待管理員審核'
   elif result == '4':
      return '資料庫錯誤，請稍後再試'
   elif result == '5':
      return '帳號驗證成功，歡迎加入我們'
   elif result == '6':
      return '帳號已驗證成功，不需再次驗證'
   elif result == '7':
      return '帳號不在資料庫中，請重新申請'
   elif result == '8':
      return '帳號驗證失敗'
   elif result == 'TimeOut':
      return '網頁已過期，請重寄驗證信'
   else:
      return '網頁出現錯誤，請稍後再試'

#審核評論
@GM.route('/updateGrade')
def update_grade():
   if session.get('userType') == userType['GM']:
      return render_template('updateGrade.html')
   else:
      return redirect(url_for('GM.login'))

#檢舉審核
@GM.route('/reportApprove')
def report_approve():
   if session.get('userType') == userType['GM']:
      return render_template('reportApprove.html')
   else:
      return redirect(url_for('GM.login'))

#設定頁面
@GM.route('/setting')
def setting():
   if session.get('userType') == userType['GM']:
      return render_template('settingGM.html')
   else:
      return redirect(url_for('GM.login'))