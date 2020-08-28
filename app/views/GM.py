#coding:utf-8
from flask import Blueprint, render_template, session, redirect, url_for
from ..models import userType

GM = Blueprint('GM', __name__)

#GM的根目錄
@GM.route('/')
def index():
   if session.get('userType') == userType['GM']:
      return redirect(url_for('GM.update_grade'))
   else:
      return redirect(url_for('GM.login'))

#忘記密碼頁面
@GM.route('/forgotPassword')
def forgot_password():
   return render_template('/GM/forgotPasswordGM.html')

#輸入新密碼頁面
@GM.route('/resetPassword/<token>')
def reset_password(token):
   return render_template('/GM/resetPasswordGM.html')

#登入頁面
@GM.route('/login')
def login():
   if session.get('userType') == userType['GM']:
      return redirect(url_for('GM.update_grade'))
   else:
      return render_template('/GM/loginGM.html')

#註冊頁面
@GM.route('/register')
def register():
   return render_template('/GM/registerGM.html')

#驗證頁面
@GM.route('/verify/<result>')
def verify(result):
   if result == '1':
      result_msg = '資料庫錯誤，請稍後再試'
   elif result == '2':
      result_msg = '資料庫錯誤，請稍後再試'
   elif result == '3':
      result_msg = '帳號驗證成功，等待管理員審核'
   elif result == '4':
      result_msg ='資料庫錯誤，請稍後再試'
   elif result == '5':
      result_msg = '帳號驗證成功，歡迎加入我們<br /><a href="' + url_for('GM.login') + '">點擊進入登入畫面</a>'
   elif result == '6':
      result_msg = '帳號已驗證成功，不需再次驗證'
   elif result == '7':
      result_msg = '帳號不在資料庫中，請重新申請'
   elif result == '8':
      result_msg = '帳號驗證失敗'
   elif result == 'TimeOut':
      result_msg = '網頁已過期，請重寄驗證信'
   else:
      result_msg = '網頁出現錯誤，請稍後再試'
   return result_msg

#評論審核
@GM.route('/updateGrade')
def update_grade():
   if session.get('userType') == userType['GM']:
      return render_template('/GM/updateGrade.html')
   else:
      return redirect(url_for('GM.login'))

#評論審核紀錄
@GM.route('/updateGradeRecord')
def update_grade_record():
   if session.get('userType') == userType['GM']:
      return render_template('/GM/updateGradeRecord.html')
   else:
      return redirect(url_for('GM.login'))

#檢舉審核
@GM.route('/reportApprove')
def report_approve():
   if session.get('userType') == userType['GM']:
      return render_template('/GM/reportApprove.html')
   else:
      return redirect(url_for('GM.login'))

#檢舉審核紀錄
@GM.route('/reportApproveRecord')
def report_approve_record():
   if session.get('userType') == userType['GM']:
      return render_template('/GM/reportApproveRecord.html')
   else:
      return redirect(url_for('GM.login'))

#設定頁面
@GM.route('/setting')
def setting():
   if session.get('userType') == userType['GM']:
      return render_template('/GM/settingGM.html')
   else:
      return redirect(url_for('GM.login'))