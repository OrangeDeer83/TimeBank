#coding:utf-8
from flask import Blueprint, render_template, session, redirect, url_for
from ..models import userType

Admin = Blueprint('Admin', __name__)

#Admin的根目錄
@Admin.route('/')
def index():
   if session.get('userType') == userType['SA']:
      return redirect(url_for('Admin.Admin_list'))
   else:
      return redirect(url_for('Admin.login'))

#忘記密碼頁面
@Admin.route('/forgotPassword')
def forgot_password():
   return render_template('/Admin/forgotPasswordAdmin.html')

#輸入新密碼
@Admin.route('/resetPassword/<token>')
def reset_password(token):
   return render_template('/Admin/resetPasswordAdmin.html')

#登入頁面
@Admin.route('/login')
def login():
   print(session.get('userType'))
   if session.get('userType') == userType['SA']:
      return redirect(url_for('Admin.Admin_list'))
   if session.get('userType') in [userType['AA'], userType['AS'], userType['AU'], userType['AG'], userType['SA']]:
      return redirect(url_for('Admin.setting'))
   else:
      return render_template('/Admin/loginAdmin.html')

#設定頁面
@Admin.route('/setting')
def setting():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/settingSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/settingAA.html')
   elif session.get('userType') == userType['AG']:
      return render_template('/Admin/settingAG.html')
   elif session.get('userType') == userType['AS']:
      return render_template('/Admin/settingAS.html')
   elif session.get('userType') == userType['AS']:
      return render_template('/Admin/settingAU.html')
   else:
      return redirect(url_for('Admin.login'))

#核准紀錄
@Admin.route('/approveRecord')
def approve_record():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/approveRecordSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/approveRecordAA.html')
   else:
      return redirect(url_for('Admin.login'))

#核准申請
@Admin.route('/approveSystem')
def approve_system():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/approveSystemSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/approveSystemAA.html')
   else:
      return redirect(url_for('Admin.login'))

#更新申請條件
@Admin.route('/updateCondition')
def update_condition():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/updateConditionSA.html')
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/updateConditionAA.html')
   else:
      return redirect(url_for('Admin.login'))

#配發點數
@Admin.route('/givePoint')
def give_point():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/givePointSA.html')
   elif session.get('userType') == userType['AS']:
      return render_template('/Admin/givePointAS.html')
   else:
      return redirect(url_for('Admin.login'))

#配發紀錄
@Admin.route('/giveRecord')
def give_record():
   if session.get('userType') == userType['SA']:
         return render_template('/Admin/giveRecordSA.html')
   elif session.get('userType') == userType['AS']:
      return render_template('/Admin/giveRecordAS.html')
   else:
      return redirect(url_for('Admin.login'))


#人事管理 - GM申請
@Admin.route('/GMApplication')
def hrmGM_application():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/hrmGMApplicationSA.html')
   elif session.get('userType') == userType['AG']:
      return render_template('/Admin/hrmGMApplicationAG.html')
   else:
      return redirect(url_for('Admin.login'))

#人事管理 - GM列表
@Admin.route('/GMList')
def GM_list():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/hrmGMRecordSA.html')
   elif session.get('userType') == userType['AG']:
      return render_template('/Admin/hrmGMRecordAG.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 人事管理 - Admin列表
@Admin.route('/AdminList')
def Admin_list():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/hrmManager.html')
   else:
      return redirect(url_for('Admin.login'))

#更新入口網站
@Admin.route('/updateWeb')
def update_web():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/updateWebSA.html')
   elif session.get('userType') == userType['AU']:
      return render_template('/Admin/updateWebAU.html')
   else:
      return redirect(url_for('Admin.login'))
