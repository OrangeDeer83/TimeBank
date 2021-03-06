#coding: utf-8
from flask import Blueprint, request, session, jsonify
import re
from sqlalchemy.sql import func
from ..models.model import *
from ..models.hash import *
from ..models.mail import GM_approve_mail
from ..models import db, userType

HRManage = Blueprint('HRManage', __name__)


#新增管理員
@HRManage.route('/create/Admin', methods=['POST'])
def create_admin():
    if request.method == 'POST':
        if session.get('userType') == userType['SA']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 403})          #非法字元
            adminType = value['adminType']
            if int(adminType) > userType['AG'] or int(adminType) < userType['AS']:
                return jsonify({"rspCode": 401})          #adminType異常
            adminName = value['adminName']
            if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", adminName) == None:
                return jsonify({"rspCode": 402})          #帳號格式不符
            adminPassword = value['adminPassword']
            if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", adminPassword) == None:
                return jsonify({"rspCode": 403})          #密碼格式不符
            try:
                query_data = adminAccount.query.filter_by(adminName = adminName).first()
            except:
                return jsonify({"rspCode": 400})          #資料庫錯誤
            if query_data == None:
                try:
                    salt = generate_salt()
                    new_adminAccount = adminAccount(adminName=adminName, adminPassword=encrypt(adminPassword, salt)\
                                                    , adminType=adminType, adminPhone=None,adminMail=None, salt=salt)
                    db.session.add(new_adminAccount)
                    db.session.commit()
                except:
                    return jsonify({"rspCode": 400})      #資料庫錯誤    
                return jsonify({"rspCode": 200})          #管理員新增成功
            else:
                return jsonify({"rspCode": 404})          #帳號重複
        else:
            return jsonify({"rspCode": 500})              #權限不符
    else:
        return jsonify({"rspCode": 300})                  #method使用錯誤


#刪除管理員
@HRManage.route('/delete/Admin', methods=['POST'])
def delete_admin():
    if request.method == 'POST':
        if session.get('userType') == userType['SA']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 404})          #非法字元
            adminID = value['adminID']
            SAID = session.get('adminID')
            try:
                SA_data = adminAccount.query.filter(adminAccount.adminID == SAID).first()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            if session.get('adminConfirm') == SA_data.adminPassword:
                try:
                    query_data = adminAccount.query.filter(adminAccount.adminID == adminID).first()
                    if query_data == None:
                        return jsonify({"rspCode": 401})  #adminID不在資料庫中，前端可能遭到竄改
                    if query_data.adminType < userType['AS'] and query_data.adminType > userType['AG']:
                        return jsonify({"rspCode": 402})      #該帳號目前不是admin
                    query_data.adminType = userType['STOP']
                    db.session.commit()
                except:
                    return jsonify({"rspCode": 400})          #資料庫錯誤
                return jsonify({"rspCode": 200})              #刪除成功
            else:
                return ({"rspCode": 403})                 #尚未輸入第一次密碼
        else:
            return jsonify({"rspCode": 500})                  #權限不符
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤


#刪除管理員密碼驗證
@HRManage.route('/delete/Admin/check_password', methods=['POST'])
def delete_Admin_check_password():
    if request.method == 'POST':
        if session.get('userType') == userType['SA']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 402})          #非法字元
            SAID = session.get('adminID')
            SAPassword = value['SAPassword']
            try:
                SA_data = adminAccount.query.filter(adminAccount.adminID == SAID).first()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            if check_same(SAPassword, SA_data.adminPassword, SA_data.salt):
                session['adminConfirm'] = SA_data.adminPassword
                return jsonify({"rspCode": 200})              #密碼驗證成功
            else:
                return jsonify({"rspCode": 401})              #密碼輸入錯誤
        else:
            return jsonify({"rspCode": 500})                  #權限不符
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤

#輸入GM申請email
@HRManage.route('/load_GM_mail', methods=['POST'])
def load_GM_mail():
    if request.method == 'POST':
        if session.get('userType') == userType['SA'] or session.get('userType') == userType['AG']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 403})          #非法字元
            GMMail = value['GMMail']
            if re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
                return ({"rspCode": 401})                     #電子郵件格式不符
            try:
                query_data = adminAccount.query.filter_by(adminMail = GMMail).first()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            if query_data and   query_data.adminType != userType['STOP']:
                return jsonify({"rspCode": 402})              #email與他人重複
            try:
                adminName = generate_salt()[:20]
                query_data = adminAccount.query.filter_by(adminName = adminName).first()
                while query_data:
                    adminName = generate_salt()[:20]
                    query_data = adminAccount.query.filter_by(adminName = adminName).first()
                new_adminAccount = adminAccount(adminName=adminName, adminPassword='None'\
                                                    , adminType=userType['GM_unverify'], adminPhone=None,\
                                                    adminMail=GMMail, salt='None')
                db.session.add(new_adminAccount)
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            return jsonify({"rspCode": 200})                  #email輸入成功
        else:
            return jsonify({"rspCode": 500})                  #權限不符
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤

#取得現有Admin列表
@HRManage.route('/Admin_list', methods=['GET'])
def Admin_list():
    if session.get('userType') == userType['SA']:
        query_data = adminAccount.query.filter(adminAccount.adminType.in_([userType['AS'], userType['AA']\
                                                , userType['AU'], userType['AG']])).all()
        Admin_list = []
        for Admin in query_data:
            Admin_list.append({"adminType": Admin.adminType, "adminName": Admin.adminName,\
                            "adminID": Admin.adminID})
        return jsonify({"rspCode": 200, "AdminList": Admin_list})         #成功
    else:
        return jsonify({"rspCode": 500})                 #權限不符

#取得現有GM列表
@HRManage.route('/GM_list', methods=['GET'])
def GM_list():
    if session.get('userType') == userType['SA'] or session.get('userType') == userType['AG']:
        query_data = adminAccount.query.filter_by(adminType = userType['GM']).all()
        GM_list = []
        for GM in query_data:
            GM_list.append({"adminID": GM.adminID, "adminName": GM.adminName, "adminPhone": GM.adminPhone, "adminMail": GM.adminMail})
        return jsonify({"rspCode": 200, "GMList": GM_list})               #成功
    else:
        return jsonify({"rspCode": 500})                    #權限不符

#取得GM申請列表
@HRManage.route('/GM_apply_list', methods=['GET'])
def GM_apply_list():
    if session.get('userType') == userType['SA'] or session.get('userType') == userType['AG']:
        query_data = adminAccount.query.filter_by(adminType = userType['GM_waiting']).all()
        apply_list = []
        for GM in query_data:
            apply_list.append({"adminID": GM.adminID, "adminName": GM.adminName, "adminPhone": GM.adminPhone, "adminMail": GM.adminMail})
        return jsonify({"rspCode": 200, "applyList": apply_list})         #成功
    else:
        return jsonify({"rspCode": 500})                 #權限不符

#同意GM申請
@HRManage.route('/approveGM', methods=['POST'])
def approveGM():
    if request.method == 'POST':
        if session.get('userType') == userType['SA'] or session.get('userType') == userType['AG']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 403})          #非法字元
            GMID = value['GMID']
            try:
                query_data = adminAccount.query.filter_by(adminID = GMID).first()
                if query_data.adminType == userType['GM_waiting']:
                    status = GM_approve_mail(query_data.adminMail)
                    query_data.adminType = userType['GM']
                    db.session.commit()
                    while status != {}:
                        status = GM_approve_mail(query_data.adminMail)
                    return jsonify({"rspCode": 200})                      #同意GM成功，且通知信寄送成功
                else:
                    return jsonify({"rspCode": 401})              #該帳號並非待審核GM，前端可能遭竄改
            except:
                return jsonify({"rspCode": 400})                  #資料庫錯誤
        else:
            return jsonify({"rspCode": 500})                      #權限不符
    else:
        return jsonify({"rspCode": 300})                          #method使用錯誤

#拒絕GM申請
@HRManage.route('/rejectGM', methods=['POST'])
def reject_GM():
    if request.method == 'POST':
        if session.get('userType') == userType['SA'] or session.get('userType') == userType['AG']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 402})          #非法字元
            GMID = value['GMID']
            try:
                query_data = adminAccount.query.filter_by(adminID = GMID).first()
                if query_data.adminType == userType['GM_waiting']:
                    db.session.delete(query_data)
                    db.session.commit()
                else:
                    return jsonify({"rspCode": 401})              #該帳號並非待審核GM，前端可能遭竄改
            except:
                return jsonify({"rspCode": 400})                  #資料庫錯誤
            return jsonify({"rspCode": 200})                      #拒絕申請GM成功
        else:
            return jsonify({"rspCode": 500})                      #權限不符
    else:
        return jsonify({"rspCode": 300})                          #method使用錯誤

#刪除GM
@HRManage.route('/delete/GM', methods=['POST'])
def delete_GM():
    if request.method == 'POST':
        if session.get('userType') == userType['SA'] or session.get('userType') == userType['AG']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 405})          #非法字元
            GMID = value['GMID']
            adminID = session.get('adminID')
            try:
                Admin_data = adminAccount.query.filter(adminAccount.adminID == adminID).first()
                if Admin_data == None:
                    return jsonify({"rspCode": 404})                  #adminID不存在
            except:
                return jsonify({"rspCode": 400})                      #資料庫錯誤
            if session.get('adminConfirm') == Admin_data.adminPassword:
                try:
                    query_data = adminAccount.query.filter(adminAccount.adminID == GMID).first()
                    if query_data == None:
                        return jsonify({"rspCode": 401})              #GMID不在資料庫中，前端可能遭到竄改
                    if query_data.adminType != userType['GM']:
                        return jsonify({"rspCode": 402})              #userType錯誤，此ID可能不是GM
                    query_data.adminType = userType['STOP']
                    db.session.commit()
                except:
                    return jsonify({"rspCode": 400})                  #資料庫錯誤
                return jsonify({"rspCode": 200})                      #刪除成功
            else:
                return ({"rspCode": 403})                             #尚未輸入第一次密碼
        else:
            return jsonify({"rspCode": 500})                          #權限不符
    else:
        return jsonify({"rspCode": 300})                              #method使用錯誤

#刪除GM密碼驗證
@HRManage.route('/delete/GM/check_password', methods=['POST'])
def delete_GM_check_password():
    if request.method == 'POST':
        if session.get('userType') == userType['SA'] or session.get('userType') == userType['AG']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 402})          #非法字元
            adminID = session.get('adminID')
            adminPassword = value['SAPassword']
            try:
                Admin_data = adminAccount.query.filter(adminAccount.adminID == adminID).first()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            if check_same(adminPassword, Admin_data.adminPassword, Admin_data.salt):
                session['adminConfirm'] = Admin_data.adminPassword
                return jsonify({"rspCode": 200})              #密碼驗證成功
            else:
                return jsonify({"rspCode": 401})              #密碼輸入錯誤
        else:
            return jsonify({"rspCode": 500})                  #權限不符
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤

#更改Admin密碼
@HRManage.route('/changePassword', methods=['POST'])
def changePassword():
    if request.method == 'POST':
        if session.get('userType') == userType['SA']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": 40})          #非法字元
            adminID = value['adminID']
            SAID = session.get('adminID')
            try:
                SA_data = adminAccount.query.filter(adminAccount.adminID == SAID).first()
            except:
                return jsonify({"rspCode": 30})              #資料庫錯誤
            if session.get('adminConfirm') == SA_data.adminPassword:
                try:
                    query_data = adminAccount.query.filter(adminAccount.adminID == adminID).first()
                    if query_data == None:
                        return jsonify({"rspCode": 41})  #adminID不在資料庫中，前端可能遭到竄改
                    if query_data.adminType < userType['AS'] and query_data.adminType > userType['AG']:
                        return jsonify({"rspCode": 42})      #該帳號目前不是admin
                    newPassword = value['newPassword']
                    salt = generate_salt()
                    query_data.salt = salt
                    query_data.adminPassword = encrypt(newPassword, salt)
                    db.session.commit()
                except:
                    return jsonify({"rspCode": 30})          #資料庫錯誤
                return jsonify({"rspCode": 20})              #刪除成功
            else:
                return ({"rspCode": 18})                 #尚未輸入第一次密碼
        else:
            return jsonify({"rspCode": 50})                  #權限不符
    else:
        return jsonify({"rspCode": 31})                      #method使用錯誤