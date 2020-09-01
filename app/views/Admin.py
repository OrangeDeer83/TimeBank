#coding:utf-8
from flask import Blueprint, render_template, session, redirect, url_for
from ..models import userType

Admin = Blueprint('Admin', __name__)

navbarSA = '/static/js/navbarSA.js'
navbarAS = '/static/js/navbarAS.js'
navbarAA = '/static/js/navbarAA.js'
navbarAU = '/static/js/navbarAU.js'
navbarAG = '/static/js/navbarAG.js'

#Admin的根目錄
@Admin.route('/')
def index():
   if session.get('userType') == userType['SA']:
      return redirect(url_for('Admin.Admin_list'))
   else:
      return redirect(url_for('Admin.login'))

#登入頁面
@Admin.route('/login')
def login():
   print(session.get('userType'))
   if session.get('userType') == userType['SA']:
      return redirect(url_for('Admin.Admin_list'))
   elif session.get('userType') == userType['AA']:
      return redirect(url_for('Admin.approve_system'))
   elif session.get('userType') == userType['AS']:
      return redirect(url_for('Admin.give_point'))
   elif session.get('userType') ==  userType['AU']:
      return redirect(url_for('Admin.update_web'))
   elif session.get('userType') ==  userType['AG']:
      return redirect(url_for('Admin.hrmGM_application'))
   else:
      return render_template('/Admin/loginAdmin.html')

#設定頁面
@Admin.route('/setting')
def setting():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/settingAdmin.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/settingAdmin.html', navbarjs = navbarAA)
   elif session.get('userType') == userType['AG']:
      return render_template('/Admin/settingAdmin.html', navbarjs = navbarAG)
   elif session.get('userType') == userType['AS']:
      return render_template('/Admin/settingAdmin.html', navbarjs = navbarAS)
   elif session.get('userType') == userType['AU']:
      return render_template('/Admin/settingAdmin.html', navbarjs = navbarAU)
   else:
      return redirect(url_for('Admin.login'))

#核准紀錄
@Admin.route('/approveRecord')
def approve_record():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/approveRecord.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/approveRecord.html', navbarjs = navbarAA)
   else:
      return redirect(url_for('Admin.login'))

#核准申請
@Admin.route('/approveSystem')
def approve_system():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/approveSystem.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/approveSystem.html', navbarjs = navbarAA)
   else:
      return redirect(url_for('Admin.login'))

#更新申請條件
@Admin.route('/updateCondition')
def update_condition():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/updateCondition.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AA']:
      return render_template('/Admin/updateCondition.html', navbarjs = navbarAA)
   else:
      return redirect(url_for('Admin.login'))

#配發點數
@Admin.route('/givePoint')
def give_point():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/givePoint.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AS']:
      return render_template('/Admin/givePoint.html', navbarjs = navbarAS)
   else:
      return redirect(url_for('Admin.login'))

#配發紀錄
@Admin.route('/giveRecord')
def give_record():
   if session.get('userType') == userType['SA']:
         return render_template('/Admin/giveRecord.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AS']:
      return render_template('/Admin/giveRecord.html', navbarjs = navbarAS)
   else:
      return redirect(url_for('Admin.login'))


#人事管理 - GM申請
@Admin.route('/GMApplication')
def hrmGM_application():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/hrmGMApplication.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AG']:
      return render_template('/Admin/hrmGMApplication.html', navbarjs = navbarAG)
   else:
      return redirect(url_for('Admin.login'))

#人事管理 - GM列表
@Admin.route('/GMList')
def GM_list():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/hrmGMRecord.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AG']:
      return render_template('/Admin/hrmGMRecord.html', navbarjs = navbarAG)
   else:
      return redirect(url_for('Admin.login'))

#SA - 人事管理 - Admin列表
@Admin.route('/AdminList')
def Admin_list():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/hrmAdmin.html')
   else:
      return redirect(url_for('Admin.login'))

#更新入口網站
@Admin.route('/updateWeb')
def update_web():
   if session.get('userType') == userType['SA']:
      return render_template('/Admin/updateWeb.html', navbarjs = navbarSA)
   elif session.get('userType') == userType['AU']:
      return render_template('/Admin/updateWeb.html', navbarjs = navbarAU)
   else:
      return redirect(url_for('Admin.login'))
