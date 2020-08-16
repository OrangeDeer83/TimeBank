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
   return render_template('loginManger5.html')

#SA - 設定頁面
@Admin.route('/SA/setting')
def SA_setting():
   if session['userType'] == userType['SA']:
      return render_template('settingSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AA - 設定頁面
@Admin.route('/AA/setting')
def AA_setting():
   if session['userType'] == userType['AA']:
      return render_template('settingAA.html')
   else:
      return redirect(url_for('Admin.login'))

#AG - 設定頁面
@Admin.route('/AG/setting')
def AG_setting():
   if session['userType'] == userType['AG']:
      return render_template('settingAG.html')
   else:
      return redirect(url_for('Admin.login'))

#AS - 設定頁面
@Admin.route('/AS/setting')
def AS_setting():
   if session['userType'] == userType['AS']:
      return render_template('settingAS.html')
   else:
      return redirect(url_for('Admin.login'))

#AU - 設定頁面
@Admin.route('/AU/setting')
def AU_setting():
   if session['userType'] == userType['AS']:
      return render_template('settingAU.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 核准紀錄
@Admin.route('/SA/approveRecord')
def SA_approveRecord():
   if session['userType'] == userType['SA']:
      return render_template('approveRecordSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AA - 核准紀錄
@Admin.route('/AA/approveRecord')
def AA_approveRecord():
   if session['userType'] == userType['AA']:
      return render_template('approveRecordAA.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 核准申請
@Admin.route('/SA/approveSystem')
def SA_approveSystem():
   if session['userType'] == userType['SA']:
      return render_template('approveSystemSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AA - 核准申請
@Admin.route('/AA/approveSystem')
def AA_approveSystem():
   if session['userType'] == userType['AA']:
      return render_template('approveSystemAA.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 更新申請條件
@Admin.route('/SA/updateCondition')
def SA_update_condition():
   if session['userType'] == userType['SA']:
      return render_template('updateConditionSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AA - 更新申請條件
@Admin.route('/AA/updateCondition')
def AA_update_condition():
   if session['userType'] == userType['AA']:
      return render_template('updateConditionAA.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 配發點數
@Admin.route('/SA/givePoint')
def SA_givePoint():
   if session['userType'] == userType['SA']:
      return render_template('givePointSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AS - 配發點數
@Admin.route('/AS/givePoint')
def AS_givePoint():
   if session['userType'] == userType['AS']:
      return render_template('givePointAS.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 配發紀錄
@Admin.route('/SA/giveRecord')
def SA_giveRecord():
   if session['userType'] == userType['SA']:
         return render_template('giveRecordSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AS - 配發紀錄
@Admin.route('/AS/giveRecord')
def AS_giveRecord():
   if session['userType'] == userType['AS']:
      return render_template('giveRecordAS.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 人事管理 - GM申請
@Admin.route('/SA/GMApplication')
def SA_hrmGM_application():
   if session['userType'] == userType['SA']:
      return render_template('hrmGMApplicationSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AG - 人事管理 - GM申請
@Admin.route('/AG/GMApplication')
def AG_hrmGM_application():
   if session['userType'] == userType['AG']:
      return render_template('hrmGMApplicationAG.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 人事管理 - GM列表
@Admin.route('/SA/GMList')
def SA_GM_list():
   if session['userType'] == userType['SA']:
      return render_template('hrmGMRecordSA.html')
   else:
      return redirect(url_for('Admin.login'))
    
#AG - 人事管理 - GM列表
@Admin.route('/AG/GMList')
def AG_GM_list():
   if session['userType'] == userType['AG']:
      return render_template('hrmGMRecordAG.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 人事管理 - Admin列表
@Admin.route('/SA/AdminList')
def SA_list():
   if session['userType'] == userType['SA']:
      return render_template('hrmManager.html')
   else:
      return redirect(url_for('Admin.login'))

#SA - 更新入口網站
@Admin.route('/SA/updateWeb')
def SA_update_web():
   if session['userType'] == userType['SA']:
      return render_template('updateWebSA.html')
   else:
      return redirect(url_for('Admin.login'))

#AA - 更新入口網站
@Admin.route('/AU/updateWeb')
def AU_update_web():
   if session['userType'] == userType['AU']:
      return render_template('updateWebAU.html')
   else:
      return redirect(url_for('Admin.login'))