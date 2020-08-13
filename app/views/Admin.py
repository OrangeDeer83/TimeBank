#coding:utf-8
from flask import Blueprint, render_template

Admin = Blueprint('Admin', __name__)

#忘記密碼頁面
@Admin.route('/forgotPassword')
def forgotPassword():
    render_template('forgotPasswordManager5.html')

#輸入新密碼
@Admin.route('/resetPassword')
def resetPassword():
    render_template('resetPasswordManager5.html')


#登入頁面
@Admin.route('/login')
def login():
    render_template('loginManger5.html')

#SA - 設定頁面
@Admin.route('/SA/setting')
def SA_setting():
    render_template('settingSA.html')

#AA - 設定頁面
@Admin.route('/AA/setting')
def AA_setting():
    render_template('settingAA.html')

#AG - 設定頁面
@Admin.route('/AG/setting')
def AG_setting():
    render_template('settingAG.html')

#AS - 設定頁面
@Admin.route('/AS/setting')
def AS_setting():
    render_template('settingAS.html')

#AU - 設定頁面
@Admin.route('/AU/setting')
def AU_setting():
    render_template('settingAU.html')

#SA - 核准紀錄
@Admin.route('/SA/approveRecord')
def SA_approveRecord():
    render_template('approveRecordSA.html')

#AA - 核准紀錄
@Admin.route('/AA/approveRecord')
def AA_approveRecord():
    render_template('approveRecordAA.html')

#SA - 核准申請
@Admin.route('/SA/approveSystem')
def SA_approveSystem():
    render_template('approveSystemSA.html')

#AA - 核准申請
@Admin.route('/AA/approveSystem')
def AA_approveSystem():
    render_template('approveSystemAA.html')

#SA - 更新申請條件
@Admin.route('/SA/updateCondition')
def SA_update_condition():
    render_template('updateConditionSA.html')

#AA - 更新申請條件
@Admin.route('/AA/updateCondition')
def AA_update_condition():
    render_template('updateConditionAA.html')

#SA - 配發點數
@Admin.route('/SA/givePoint')
def SA_givePoint():
    render_template('givePointSA.html')

#AS - 配發點數
@Admin.route('/AS/givePoint')
def AS_givePoint():
    render_template('givePointAS.html')

#SA - 配發紀錄
@Admin.route('/SA/giveRecord')
def SA_giveRecord():
    render_template('giveRecordSA.html')

#AS - 配發紀錄
@Admin.route('/AS/giveRecord')
def AS_giveRecord():
    render_template('giveRecordAS.html')

#SA - 人事管理 - GM申請
@Admin.route('/SA/GMApplication')
def SA_hrmGM_application():
    render_template('hrmGMApplicationSA.html')

#AG - 人事管理 - GM申請
@Admin.route('/AG/GMApplication')
def AG_hrmGM_application():
    render_template('hrmGMApplicationAG.html')

#SA - 人事管理 - GM列表
@Admin.route('/SA/GMList')
def SA_GM_list():
    render_template('hrmGMRecordSA.html')
    
#AG - 人事管理 - GM列表
@Admin.route('/AG/GMList')
def AG_GM_list():
    render_template('hrmGMRecordAG.html')

#SA - 人事管理 - Admin列表
@Admin.route('/SA/AdminList')
def SA_list():
    render_template('hrmManager.html')

#SA - 更新入口網站
@Admin.route('/SA/updateWeb')
def SA_update_web():
    render_template('updateWebSA.html')

#AA - 更新入口網站
@Admin.route('/AU/updateWeb')
def AU_update_web():
    render_template('updateWebAU.html')