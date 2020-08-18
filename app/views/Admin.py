#coding:utf-8
from flask import Blueprint, render_template, session, redirect, url_for
from ..models import userType

Admin = Blueprint('Admin', __name__)

#忘記密碼頁面
@Admin.route('/forgotPassword')
def forgot_password():
   return render_template('forgotPasswordManager5.html')

#輸入新密碼
@Admin.route('/resetPassword/<token>')
def reset_password(token):
   return render_template('resetPasswordManager5.html')

#登入頁面
@Admin.route('/login')
def login():
   print(session.get('userType'))
   if session.get('userType') in [userType['AA'], userType['AS'], userType['AU'], userType['AG'], userType['SA']]:
      return redirect(url_for('Admin.setting'))
   else:
      return render_template('loginManager5.html')

#設定頁面
@Admin.route('/setting')
def setting():
   print(session.get('userType'))
   if session.get('userType') == userType['SA']:
      return render_template('settingSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('settingAA.html')
   elif session.get('userType') == userType['AG']:
      return render_template('settingAG.html')
   elif session.get('userType') == userType['AS']:
      return render_template('settingAS.html')
   elif session.get('userType') == userType['AS']:
      return render_template('settingAU.html')
   else:
      return redirect(url_for('Admin.login'))

#核准紀錄
@Admin.route('/approveRecord')
def approveRecord():
   if session.get('userType') == userType['SA']:
      return render_template('approveRecordSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('approveRecordAA.html')
   else:
      return redirect(url_for('Admin.login'))

#核准申請
@Admin.route('/approveSystem')
def approveSystem():
   if session.get('userType') == userType['SA']:
      return render_template('approveSystemSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('approveSystemAA.html')
   else:
      return redirect(url_for('Admin.login'))

#更新申請條件
@Admin.route('/updateCondition')
def update_condition():
   if session.get('userType') == userType['SA']:
      return render_template('updateConditionSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('updateConditionAA.html')
   else:
      return redirect(url_for('Admin.login'))

#配發點數
@Admin.route('/givePoint')
def give_point():
   if session.get('userType') == userType['SA']:
      return render_template('givePointSA.html')
   elif session.get('userType') == userType['AS']:
      return render_template('givePointAS.html')
   else:
      return redirect(url_for('Admin.login'))

#配發紀錄
@Admin.route('/giveRecord')
def give_record():
   if session.get('userType') == userType['SA']:
         return render_template('giveRecordSA.html')
   elif session.get('userType') == userType['AS']:
      return render_template('giveRecordAS.html')
   else:
      return redirect(url_for('Admin.login'))


#人事管理 - GM申請
@Admin.route('/GMApplication')
def hrmGM_application():
   if session.get('userType') == userType['SA']:
      return render_template('hrmGMApplicationSA.html')
   elif session.get('userType') == userType['AG']:
      return render_template('hrmGMApplicationAG.html')
   else:
      return redirect(url_for('Admin.login'))

#人事管理 - GM列表
@Admin.route('/GMList')
def GM_list():
   if session.get('userType') == userType['SA']:
      return render_template('hrmGMRecordSA.html')
   elif session.get('userType') == userType['AG']:
      return render_template('hrmGMRecordAG.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 人事管理 - Admin列表
@Admin.route('/SA/AdminList')
def SA_list():
   if session.get('userType') == userType['SA']:
      return render_template('hrmManager.html')
   else:
      return redirect(url_for('Admin.login'))

#更新入口網站
@Admin.route('/updateWeb')
def SA_update_web():
   if session.get('userType') == userType['SA']:
      return render_template('updateWebSA.html')
   elif session.get('userType') == userType['AU']:
      return render_template('updateWebAU.html')
   else:
      return redirect(url_for('Admin.login'))
