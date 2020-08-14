#coding:utf-8
from flask import Blueprint, render_template

Admin = Blueprint('Admin', __name__)

#忘記密碼頁面
@Admin.route('/forgotPassword')
def forgot_password():
   return render_template('forgotPasswordManager5.html')

#輸入新密碼
@Admin.route('/resetPassword')
def reset_password():
   return render_template('resetPasswordManager5.html')


#登入頁面
@Admin.route('/login')
def login():
   return render_template('loginManger5.html')

#SA - 設定頁面
@Admin.route('/SA/setting')
def SA_setting():
   return render_template('settingSA.html')

#AA - 設定頁面
@Admin.route('/AA/setting')
def AA_setting():
   return render_template('settingAA.html')

#AG - 設定頁面
@Admin.route('/AG/setting')
def AG_setting():
   return render_template('settingAG.html')

#AS - 設定頁面
@Admin.route('/AS/setting')
def AS_setting():
   return render_template('settingAS.html')

#AU - 設定頁面
@Admin.route('/AU/setting')
def AU_setting():
   return render_template('settingAU.html')

#SA - 核准紀錄
@Admin.route('/SA/approveRecord')
def SA_approveRecord():
   return render_template('approveRecordSA.html')

#AA - 核准紀錄
@Admin.route('/AA/approveRecord')
def AA_approveRecord():
   return render_template('approveRecordAA.html')

#SA - 核准申請
@Admin.route('/SA/approveSystem')
def SA_approveSystem():
   return render_template('approveSystemSA.html')

#AA - 核准申請
@Admin.route('/AA/approveSystem')
def AA_approveSystem():
   return render_template('approveSystemAA.html')

#SA - 更新申請條件
@Admin.route('/SA/updateCondition')
def SA_update_condition():
   return render_template('updateConditionSA.html')

#AA - 更新申請條件
@Admin.route('/AA/updateCondition')
def AA_update_condition():
   return render_template('updateConditionAA.html')

#SA - 配發點數
@Admin.route('/SA/givePoint')
def SA_givePoint():
   return render_template('givePointSA.html')

#AS - 配發點數
@Admin.route('/AS/givePoint')
def AS_givePoint():
   return render_template('givePointAS.html')

#SA - 配發紀錄
@Admin.route('/SA/giveRecord')
def SA_giveRecord():
   return render_template('giveRecordSA.html')

#AS - 配發紀錄
@Admin.route('/AS/giveRecord')
def AS_giveRecord():
   return render_template('giveRecordAS.html')

#SA - 人事管理 - GM申請
@Admin.route('/SA/GMApplication')
def SA_hrmGM_application():
   return render_template('hrmGMApplicationSA.html')

#AG - 人事管理 - GM申請
@Admin.route('/AG/GMApplication')
def AG_hrmGM_application():
   return render_template('hrmGMApplicationAG.html')

#SA - 人事管理 - GM列表
@Admin.route('/SA/GMList')
def SA_GM_list():
   return render_template('hrmGMRecordSA.html')
    
#AG - 人事管理 - GM列表
@Admin.route('/AG/GMList')
def AG_GM_list():
   return render_template('hrmGMRecordAG.html')

#SA - 人事管理 - Admin列表
@Admin.route('/SA/AdminList')
def SA_list():
   return render_template('hrmManager.html')

#SA - 更新入口網站
@Admin.route('/SA/updateWeb')
def SA_update_web():
   return render_template('updateWebSA.html')

#AA - 更新入口網站
@Admin.route('/AU/updateWeb')
def AU_update_web():
   return render_template('updateWebAU.html')