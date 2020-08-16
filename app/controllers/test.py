#coding: utf-8
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, current_app
import re, datetime, smtplib
from sqlalchemy.sql import func
from math import floor
from ..models.model import *
from ..models.dao import *
from ..models.hash import *
from ..models.token import *
from ..models.mail import *
from ..models import db, userType
from email.mime.text import MIMEText
import os
import datetime
test = Blueprint('test', __name__)

#設定時間格式
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

#偵測一般使用者帳號重複(註冊用)
@test.route('/USER/detect_repeated', methods=['POST'])
def USER_detect_repeated():
    if request.method == 'POST':
        value = request.get_json()
        userName = value['userName']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", userName) == None:
            return jsonify({"rspCode": "401"})  #帳號格式不符
        else:
            try:
                query_data = account.query.filter(account.userName == func.binary(userName)).first()
            except:
                return jsonify({"rspCode": "400"})  #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": "200"})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": "402"})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

#一般使用者註冊
@test.route('/USER/register', methods=['POST'])
def USER_register():
    if request.method == 'POST':
        value = request.get_json()
        user = []
        user.append(value['name'])
        user.append(value['userName'])
        user.append(value['userPassword'])
        user.append(value['userMail'])
        user.append(value['userPhone'])
        user.append(value['userGender'])
        user.append(value['userBirthday'])
        if len(user[0]) > 20 or len(user[0]) < 1:
            return jsonify({"rspCode": "401"})      #名稱長度不符
        elif re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", user[1]) == None:
            return jsonify({"rspCode": "402"})      #帳號格式不符
        elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", user[2]) == None:
            return jsonify({"rspCode": "403"})      #密碼格式不符
        elif len(user[3]) > 50 or len(user[3]) < 1:
            return jsonify({"rspCode": "404"})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", user[3]) == None:
            return jsonify({"rspCode": "405"})      #電子郵件格式不符
        elif re.search(r"^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$", user[4]) == None:
            return jsonify({"rspCode": "406"})      #手機號碼格式不符
        elif int(user[5]) > 2 or int(user[5]) < 0:
            return jsonify({"rspCode": "407"})       #性別異常
        elif re.search(r"^((18|19|20)[0-9]{2})[-\/.](0?[1-9]|1[012])[-\/.](0?[1-9]|[12][0-9]|3[01])$", user[6]) == None:
            return jsonify({"rspCode": "408"})       #生日格式不符
        else:
            today = datetime.date.today()
            other_day = datetime.date(int(user[6][0:4]), int(user[6][5:7]), int(user[6][8:10]))
            result = other_day - today
            if result.days > 0:
                return jsonify({"rspCode": "409"})  #未來人錯誤
            else:
                try:
                    existName = account.query.filter(account.userName == func.binary(user[1])).first()
                    existMail = account.query.filter(account.userMail == func.binary(user[3])).first()
                except:
                    return jsonify({"rspCode": "400"})      #資料庫錯誤
                if existName:
                    return jsonify({"rspCode": "410"})      #帳號重複
                elif existMail:
                    return jsonify({"rspCode": "411"})      #電子郵件重複
                else:
                    try:
                        salt = generate_salt()
                        new_account = account(userName=user[1], name=user[0], userPassword=encrypt(user[2], salt),\
                                userMail=user[3], userPhone=user[4], userInfo=None, userPoint=0,\
                                SRRate=None, SRRateTimes=0, SPRate=None, SPRateTimes=0, userGender=user[5],\
                                userBirthday=user[6], salt=salt)
                        print(new_account.userPassword)
                        db.session.add(new_account)
                        db.session.commit()
                    except:
                        return jsonify({"rspCode": "400"})  #資料庫錯誤
            return jsonify({"rspCode": "200"})          #成功註冊
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

#一般使用者登入
@test.route('/USER/login', methods=['POST'])
def USER_login():
    if request.method == 'POST':
        value = request.get_json()
        print(value) 
        userName = value['userName']
        userPassword = value['userPassword']
        try:
            query_data = account.query.filter(account.userName == func.binary(userName)).first()
            print(query_data)
        except:
            return jsonify({"rspCode": "400"})   #資料庫錯誤
        if query_data == None:    
            return jsonify({"rspCode": "401"})   #登入失敗，沒有該帳號
        if check_same(userPassword, query_data.userPassword, query_data.salt):
            session['userID'] = query_data.userID
            session['userType'] = 1
            return jsonify({"rspCode": "200"}) #登入成功
        else:
            return jsonify({"rspCode": "402"}) #登入失敗，密碼錯誤
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

#登出
@test.route('/logout')
def logout():
    if session.get('userID'):
        session.clear()
        return jsonify({"rspCode": "200"})  #登出成功
    else:
        return jsonify({"rspCode": "400"})  #登出失敗

#一般使用者申請重設密碼信
@test.route('/USER/forgot_password', methods=['POST'])
def USER_forgot_password():
    if request.method == 'POST':
        value = request.get_json()
        userMail = value['userMail']
        print(value)
        if len(userMail) > 50 or len(userMail) < 1:
            return ({"rspCode": "401"})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", userMail) == None:
            return ({"rspCode": "402"})      #電子郵件格式不符
        else:
            try:
                query_data = account.query.filter(account.userMail == func.binary(userMail)).first()
            except:
                return jsonify({"rspCode": "400"})      #資料庫錯誤
            print(query_data)
            if query_data:
                userID = query_data.userID
                #產生token
                token = USER_forgot_password_token(current_app.config['SECRET_KEY'], userID)
                token_cut = str(token).split("'")[1]
                '''
                #撰寫信件
                mime = MIMEText("點擊以下連結以重設密碼\nhttp://192.168.1.146:5000" +\
                    url_for('test.reset_password_page', token=token_cut), "plain", "utf-8")     #內文
                mime["Subject"] = "TimeBank - 重設密碼"                                         #標題
                #mime["From"] = "steven200083@gmail.com"                                        #寄件人
                mime["To"] = userMail                                                           #收件人
                msg = mime.as_string()                                                          #轉字串
                #設定SMTP
                smtp=smtplib.SMTP('smtp.gmail.com', 587)
                smtp.ehlo()
                smtp.starttls()
                smtp.login('steven200083@gmail.com','itzqgclbfpojylmw')
                from_addr = 'noreply@timeBank.com'
                to_addr = userMail
                status = smtp.sendmail(from_addr, to_addr, msg)'''
                status = USER_forgot_password_mail(token_cut, userMail)
                if status == {}:
                    print("寄信成功\n")
                    return ({"rspCode": "200"})     #重置信寄送成功
                else:
                    print("寄信失敗\n"  )
                    return ({"rspCode": "404"})     #重置信寄送失敗
            else:
                return ({"rspCode": "403"})         #電子郵件輸入錯誤，沒有找到對應的電子郵件
            
    else:
        return ({"rspCode": "300"})         #methods使用錯誤

#一般使用者重設密碼
@test.route('/USER/reset_password/<token>', methods=['POST'])
def USER_reset_password(token):
    if request.method == 'POST':
        value = request.get_json()
        print(value)
        token_data = validate_token(current_app.config['SECRET_KEY'], token)
        if token_data:
            userPassword = value['userPassword']
            if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,30}$", userPassword) == None:
                return jsonify({"rspCode": "402"})      #密碼格式不符
            else:
                try:
                    update_account = account.query.filter(account.userID == func.binary(token_data['userID'])).first()
                    salt = generate_salt()
                    update_account.userPassword = encrypt(userPassword, salt)
                    update_account.salt = salt
                    db.session.commit()
                except:
                    print(400)
                    return jsonify({"rspCode": "400"})          #資料庫錯誤
                print(200)
                return jsonify({"rspCode": "200"})              #重設密碼成功
        else:
            print(401)
            return jsonify({"rspCode": "401"})                  #token驗證失敗
    else:
        print(300)
        return jsonify({"rspCode": "300"})                      #method使用錯誤


#偵測管理員帳號重複(管理員用)
@test.route('/Admin/detect_repeated', methods=['POST'])
def sa_detect_repeated():
    if request.method == 'POST':
        value = request.get_json()
        adminName = value['adminName']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", adminName) == None:
            return jsonify({"rspCode": "401"})  #帳號格式不符
        else:
            try:
                query_data = adminAccount.query.filter(adminAccount.adminName == func.binary(adminName)).first()
            except:
                return jsonify({"rspCode": "400"})  #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": "200"})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": "402"})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

#新增管理員
@test.route('/create/Admin', methods=['POST'])
def create_admin():
    if request.method == 'POST':
        value = request.get_json()
        print(value)
        adminType = value['adminType']
        if int(adminType) > userType['AG'] or int(adminType) < userType['AS']:
            return jsonify({"rspCode": "401"})          #adminType異常
        adminName = value['adminName']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", adminName) == None:
            return jsonify({"rspCode": "402"})          #帳號格式不符
        adminPassword = value['adminPassword']
        if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", adminPassword) == None:
            return jsonify({"rspCode": "403"})          #密碼格式不符
        try:
            query_data = adminAccount.query.filter(adminAccount.adminName == func.binary(adminName)).first()
            print(query_data)
        except:
            return jsonify({"rspCode": "400"})          #資料庫錯誤
        if query_data == None:
            try:
                salt = generate_salt()
                print(salt)
                new_adminAccount = adminAccount(adminName=adminName, adminPassword=encrypt(adminPassword, salt)\
                                                , adminType=adminType, adminPhone=None,adminMail=None, salt=salt)
                print(new_adminAccount)
                db.session.add(new_adminAccount)
                db.session.commit()
            except:
                return jsonify({"rspCode": "400"})      #資料庫錯誤    
            return jsonify({"rspCode": "200"})          #管理員新增成功
        else:
            return jsonify({"rspCode": "404"})          #帳號重複
    else:
        return jsonify({"rspCode": "300"})              #method使用錯誤

#刪除管理員
@test.route('/delete/Admin', methods=['POST'])
def delete_admin():
    if request.method == 'POST':
        value = request.get_json()
        adminID = value['adminID']
        SAID = value['SAID']
        try:
            SA_data = adminAccount.query.filter(adminAccount.adminID == SAID).first()
            if SA_data == None:
                return jsonify({"rspCode": "403"})              #SAID錯誤
        except:
            return jsonify({"rspCode": "400"})              #資料庫錯誤
        print(session.get('AdminConfirm'))
        if session.get('AdminConfirm') == SA_data.adminPassword:
            try:
                query_data = adminAccount.query.filter(adminAccount.adminID == adminID).first()
                if query_data == None:
                    return jsonify({"rspCode": "401"})      #adminID不在資料庫中，前端可能遭到竄改
                if query_data.adminType < userType['AS'] and query_data.adminType > userType['AG']:
                    return jsonify({"rspCode": "402"})      #該帳號目前不是admin
                query_data.adminType = userType['STOP']
                db.session.commit()
            except:
                return jsonify({"rspCode": "400"})          #資料庫錯誤
            return jsonify({"rspCode": "200"})              #刪除成功
        else:
            return jsonify({"rspCode": "403"})              #尚未輸入第一次密碼
    else:
        return jsonify({"rspCode": "300"})                  #method使用錯誤

#刪除管理員密碼驗證
@test.route('/delete/Admin/check_password', methods=['POST'])
def delete_Admin_check_password():
    if request.method == 'POST':
        value = request.get_json()
        SAID = value['SAID']
        SAPassword = value['SAPassword']
        try:
            SA_data = adminAccount.query.filter(adminAccount.adminID == SAID).first()
            if SA_data == None:
                return jsonify({"rspCode": "402"})              #SAID錯誤
        except:
            return jsonify({"rspCode": "400"})              #資料庫錯誤
        if check_same(SAPassword, SA_data.adminPassword, SA_data.salt):
            session['AdminConfirm'] = SA_data.adminPassword
            return jsonify({"rspCode": "200"})              #密碼驗證成功
        else:
            return jsonify({"rspCode": "401"})              #密碼輸入錯誤

#輸入GM申請email
@test.route('/load_GM_mail', methods=['POST'])
def load_GM_mail():
    if request.method == 'POST':
        value = request.get_json()
        GMMail = value['GMMail']
        if re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
            return ({"rspCode": "401"})                     #電子郵件格式不符
        try:
            query_data = adminAccount.query.filter_by(adminMail = GMMail).first()
        except:
            return jsonify({"rspCode": "400"})              #資料庫錯誤
        if query_data:
            return jsonify({"rspCode": "402"})              #email與他人重複
        try:
            adminName = generate_salt()
            query_data = adminAccount.query.filter_by(adminName = adminName[:20]).first()
            while query_data:
                adminName = generate_salt()
                query_data = adminAccount.query.filter_by(adminName = adminName[:20]).first()
            new_adminAccount = adminAccount(adminName=adminName[:20], adminPassword='None'\
                                            , adminType=userType['GM_unverify'], adminPhone=None,\
                                            adminMail=GMMail, salt='None')
            db.session.add(new_adminAccount)
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})              #資料庫錯誤
        return jsonify({"rspCode": "200"})                  #email輸入成功
    else:
        return jsonify({"rspCode": "300"})                  #method使用錯誤

#GM註冊
@test.route('/GM/register', methods=['POST'])
def GM_register():
    if request.method == 'POST':
        value = request.get_json()
        GMName = value['GMName']
        GMPassword = value['GMPassword']
        GMMail = value['GMMail']
        GMPhone = value['GMPhone']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", GMName) == None:
            return jsonify({"rspCode": "401"})                  #帳號格式不符
        elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", GMPassword) == None:
            return jsonify({"rspCode": "402"})                  #密碼格式不符
        elif len(GMMail) > 50 or len(GMMail) < 1:
            return jsonify({"rspCode": "403"})                  #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
            return jsonify({"rspCode": "404"})                  #電子郵件格式不符
        elif re.search(r"^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$", GMPhone) == None:
            return jsonify({"rspCode": "405"})                  #手機號碼格式不符
        else:
            try:
                existName = adminAccount.query.filter(adminAccount.adminName == func.binary(GMName)).first()
                existMail = adminAccount.query.filter(adminAccount.adminMail == func.binary(GMMail)).first()
            except:
                return jsonify({"rspCode": "400"})              #資料庫錯誤
            if existName:
                if existName != existMail:
                    return jsonify({"rspCode": "406"})          #帳號與他人重複
            if existMail:
                if existMail.adminType == userType['GM_unverify']:
                    try:
                        salt = generate_salt()
                        existMail.adminName = GMName
                        existMail.adminPassword = encrypt(GMPassword, salt)
                        existMail.adminPhone = GMPhone
                        existMail.salt = salt
                        db.session.commit()
                    except:
                        return jsonify({"rspCode": "400"})      #資料庫錯誤
                    token = GM_verify_token(current_app.config['SECRET_KEY'], existMail.adminID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token_cut, GMMail)
                    if status == {}:
                        print("寄信成功\n")
                        return ({"rspCode": "200"})             #電子郵件已被輸入，驗證信寄送成功
                    else:
                        print("寄信失敗\n")
                        return ({"rspCode": "407"})             #驗證信寄送失敗
                elif existMail.adminType == userType['GM_apply']:
                    token = GM_verify_token(current_app.config['SECRET_KEY'], existMail.adminID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token_cut, GMMail)
                    if status == {}:
                        print("寄信成功\n")
                        return ({"rspCode": "201"})             #電子郵件已申請過，驗證信再次寄出
                    else:
                        print("寄信失敗\n"  )
                        return ({"rspCode": "408"})             #驗證信寄送失敗
                else:
                    return jsonify({"rspCode": "409"})          #電子郵件與他人重複
            else:
                try:
                    salt = generate_salt()
                    new_adminAccount = adminAccount(adminName=GMName, adminPassword=encrypt(GMPassword, salt),\
                                                    adminType=userType['GM_apply'], adminPhone=GMPhone, adminMail=GMMail, salt=salt)
                    db.session.add(new_adminAccount)
                    db.session.commit()
                except:
                    return jsonify({"rspCode": "400"})          #資料庫錯誤
                token = GM_verify_token(current_app.config['SECRET_KEY'], new_adminAccount.adminID)
                token_cut = str(token).split("'")[1]
                status = GM_verify_mail(token, GMMail)
                if status == {}:
                    print("寄信成功\n")
                    return ({"rspCode": "202"})                 #帳號申請成功，驗證信已寄出
                else:
                    print("寄信失敗\n"  )
                    return ({"rspCode": "410"})                 #驗證信寄送失敗
    else:
        return ({"rspCode": "300"})                             #method使用錯誤

#同意GM申請
@test.route('/approveGM', methods=['POST'])
def approve_GM():
    if request.method == 'POST':
        value = request.get_json()
        GMID = value['GMID']
        try:
            query_data = adminAccount.query.filter_by(adminID = GMID).first()
            if query_data.adminType == userType['GM_waiting']:
                query_data.adminType = userType['GM']
                db.session.commit()
            else:
                return jsonify({"rspCode": "401"})              #該帳號並非待審核GM，前端可能遭竄改
        except:
            return jsonify({"rspCode": "400"})                  #資料庫錯誤
        return jsonify({"rspCode": "200"})                      #同意GM申請成功
    else:
        return jsonify({"rspCode": "300"})                      #method使用錯誤

#拒絕GM申請
@test.route('/rejectGM', methods=['POST'])
def reject_GM():
    if request.method == 'POST':
        value = request.get_json()
        GMID = value['GMID']
        try:
            query_data = adminAccount.query.filter_by(adminID = GMID).first()
            if query_data.adminType == userType['GM_waiting']:
                db.session.delete(query_data)
                db.session.commit()
            else:
                return jsonify({"rspCode": "401"})              #該帳號並非待審核GM，前端可能遭竄改
        except:
            return jsonify({"rspCode": "400"})                  #資料庫錯誤
        return jsonify({"rspCode": "200"})                      #拒絕申請GM成功
    else:
        return jsonify({"rspCode": "300"})                      #method使用錯誤

#管理員登入
@test.route('/Admin/login', methods=['POST'])
def Admin_login():
    if request.method == 'POST':
        value = request.get_json()
        adminName = value['adminName']
        adminPassword = value['adminPassword']
        try:
            query_data = adminAccount.query.filter(adminAccount.adminName == func.binary(adminName)).first()
        except:
            return jsonify({"rspCode": "400"})                  #資料庫錯誤
        if query_data == None:
            return jsonify({"rspCode": "401"})                  #登入失敗，沒有該帳號
        if check_same(adminPassword, query_data.adminPassword, query_data.salt) and\
                    query_data.adminType < userType['USER_unverify'] and\
                    query_data.adminType > userType['USER']:
            session['adminID'] = query_data.adminID
            session['userType'] = query_data.adminType
            return jsonify({"rspCode": "200"})                  #登入成功
        else:
            return jsonify({"rspCode": "402"})                  #登入失敗，密碼錯誤
    else:
        return jsonify({"rspCode": "300"})                      #method使用錯誤

#取得現有Admin列表
@test.route('/Admin_list', methods=['GET'])
def Admin_list():
    query_data = adminAccount.query.filter(adminAccount.adminType.in_(\
                    [userType['AS'], userType['AA'], userType['AU'], userType['AG']]))
    Admin_list = []
    for Admin in query_data:
        Admin_list.append({"adminType": Admin.adminType, "adminName": Admin.adminName,\
                        "adminID": Admin.adminID, "adminPhone": Admin.adminPhone, "adminMail": Admin.adminMail})
    return jsonify({"rspCode": "200", "AdminList": Admin_list})

#取得GM申請列表
@test.route('/GM_apply_list', methods=['GET'])
def GM_apply_list():
    query_data = adminAccount.query.filter_by(adminType = userType['GM_waiting']).all()
    apply_list = []
    for GM in query_data:
        apply_list.append({"adminID": GM.adminID, "adminName": GM.adminName, "adminPhone": GM.adminPhone, "adminMail": GM.adminMail})
    
    return jsonify({"rspCode": "200", "applyList": apply_list})

#取得現有GM列表
@test.route('/GM_list', methods=['GET'])
def GM_list():
    query_data = adminAccount.query.filter_by(adminType = userType['GM']).all()
    GM_list = []
    for GM in query_data:
        GM_list.append({"adminID": GM.adminID, "adminName": GM.adminName, "adminPhone": GM.adminPhone, "adminMail": GM.adminMail})
    return jsonify({"rspCode": "200", "GMList": GM_list})               #成功  

#刪除GM
@test.route('/delete/GM', methods=['POST'])
def delete_GM():
    if request.method == 'POST':
        value = request.get_json()
        GMID = value['GMID']
        adminID = value['adminID']
        try:
            Admin_data = adminAccount.query.filter(adminAccount.adminID == adminID).first()
            if Admin_data == None:
                return jsonify({"rspCode": "404"})                  #該帳號不是Admin帳號
        except:
            return jsonify({"rspCode": "400"})                      #資料庫錯誤
        print(Admin_data.adminPassword)
        #if session.get('AdminConfirm') == Admin_data.adminPassword:
        try:
            query_data = adminAccount.query.filter(adminAccount.adminID == GMID).first()
            if query_data == None:
                return jsonify({"rspCode": "401"})              #GMID不在資料庫中，前端可能遭到竄改
            if query_data.adminType != userType['GM']:
                return jsonify({"rspCode": "402"})              #userType錯誤，此ID可能不是GM
            query_data.adminType = userType['STOP']
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})                  #資料庫錯誤
        return jsonify({"rspCode": "200"})                      #刪除成功
        #else:
        #    return jsonify({"rspCode": "403"})                         #尚未輸入第一次密碼
    else:
        return jsonify({"rspCode": "300"})                      #method使用錯誤

#刪除GM密碼驗證
@test.route('delete/GM/check_password', methods=['POST'])
def delete_GM_check_password():
    if request.method == 'POST':
        value = request.get_json()
        adminID = value['adminID']
        adminPassword = value['adminPassword']
        try:
            Admin_data = adminAccount.query.filter(adminAccount.adminID == adminID).first()
        except:
            return jsonify({"rspCode": "400"})                      #資料庫錯誤
        if check_same(adminPassword, Admin_data.adminPassword, Admin_data.salt):
            session['AdminConfirm'] = Admin_data.adminPassword
            return jsonify({"rspCode": "200"})                  #密碼驗證成功
        else:
            return jsonify({"rspCode": "404"})                  #密碼輸入錯誤

#管理員申請重設密碼信
@test.route('/Admin/forgot_password', methods=['POST'])
def Admin_forgot_password():
    if request.method == 'POST':
        value = request.get_json()
        adminMail = value['adminMail']
        print(value)
        if len(adminMail) > 50 or len(adminMail) < 1:
            return ({"rspCode": "401"})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", adminMail) == None:
            return ({"rspCode": "402"})      #電子郵件格式不符
        else:
            try:
                query_data = adminAccount.query.filter(adminAccount.adminMail == func.binary(adminMail)).first()
            except:
                return jsonify({"rspCode": "400"})      #資料庫錯誤
            print(query_data)
            if query_data:
                adminID = query_data.adminID
                #產生token
                token = Admin_forgot_password_token(current_app.config['SECRET_KEY'], adminID)
                token_cut = str(token).split("'")[1]
                status = Admin_forgot_password_mail(token_cut, adminMail)
                if status == {}:
                    print("寄信成功\n")
                    return ({"rspCode": "200"})     #重置信寄送成功
                else:
                    print("寄信失敗\n"  )
                    return ({"rspCode": "404"})     #重置信寄送失敗
            else:
                return ({"rspCode": "403"})         #電子郵件輸入錯誤，沒有找到對應的電子郵件
    else:
        return ({"rspCode": "300"})         #methods使用錯誤

#管理員重設密碼
@test.route('/Admin/reset_password/<token>', methods=['POST'])
def Admin_reset_password(token):
    if request.method == 'POST':
        value = request.get_json()
        print(value)
        token_data = validate_token(current_app.config['SECRET_KEY'], token)
        try:
            adminID = token_data['adminID']
        except:
            return jsonify({"rspCode": "401"})                  #token驗證失敗
        adminPassword = value['adminPassword']
        if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,30}$", adminPassword) == None:
            return jsonify({"rspCode": "402"})                  #密碼格式不符
        else:                    
            try:
                update_adminAccount = adminAccount.query.filter(adminAccount.adminID == adminID).first()
                salt = generate_salt()
                update_adminAccount.adminPassword = encrypt(adminPassword, salt)
                update_adminAccount.salt = salt
                db.session.commit()
            except:
                return jsonify({"rspCode": "400"})              #資料庫錯誤
            return jsonify({"rspCode": "200"})                  #重設密碼成功
    else:
        print(300)
        return jsonify({"rspCode": "300"})                      #method使用錯誤

#GM申請重設密碼信
@test.route('/GM/forgot_password', methods=['POST'])
def GM_forgot_password():
    if request.method == 'POST':
        value = request.get_json()
        GMMail = value['GMMail']
        print(value)
        if len(GMMail) > 50 or len(GMMail) < 1:
            return ({"rspCode": "401"})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
            return ({"rspCode": "402"})      #電子郵件格式不符
        else:
            try:
                query_data = adminAccount.query.filter(adminAccount.adminMail == GMMail).first()
            except:
                return jsonify({"rspCode": "400"})      #資料庫錯誤
            if query_data:
                adminID = query_data.adminID
                #產生token
                token = GM_forgot_password_token(current_app.config['SECRET_KEY'], adminID)
                token_cut = str(token).split("'")[1]
                status = GM_forgot_password_mail(token_cut, GMMail)
                if status == {}:
                    print("寄信成功\n")
                    return ({"rspCode": "200"})     #重置信寄送成功
                else:
                    print("寄信失敗\n"  )
                    return ({"rspCode": "404"})     #重置信寄送失敗
            else:
                return ({"rspCode": "403"})         #電子郵件輸入錯誤，沒有找到對應的電子郵件
    else:
        return ({"rspCode": "300"})         #methods使用錯誤

#GM重設密碼
@test.route('/GM/reset_password/<token>', methods=['POST'])
def GM_reset_password(token):
    if request.method == 'POST':
        value = request.get_json()
        print(value)
        token_data = validate_token(current_app.config['SECRET_KEY'], token)
        try:
            GMID = token_data['GMID']
        except:
            return jsonify({"rspCode": "401"})                  #token驗證失敗
        GMPassword = value['GMPassword']
        if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,30}$", GMPassword) == None:
            return jsonify({"rspCode": "402"})                  #密碼格式不符
        else:                    
            try:
                update_adminAccount = adminAccount.query.filter(adminAccount.adminID == GMID).first()
                salt = generate_salt()
                update_adminAccount.adminPassword = encrypt(GMPassword, salt)
                update_adminAccount.salt = salt
                db.session.commit()
            except:
                return jsonify({"rspCode": "400"})              #資料庫錯誤
            return jsonify({"rspCode": "200"})                  #重設密碼成功
    else:
        print(300)
        return jsonify({"rspCode": "300"})                      #method使用錯誤

#設定使用者介紹
@test.route('/setting/userInfo', methods=['POST'])
def setting_userInfo():
    if request.method == 'POST':
        userInfo = request.get_json()['userInfo']
        userID = request.get_json()['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
            query_data.userInfo = userInfo
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        return jsonify({"rspCode": "200"})          #使用者介紹修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤

#設定名稱
@test.route('/setting/name', methods=['POST'])
def setting_name():
    if request.method == 'POST':
        name = request.get_json()['name']
        userID = request.get_json()['userID']
        if len(name) > 20 or len(name) < 1:
            return jsonify({"rspCode": "401"})      #名稱長度不符
        try:
            query_data = account.query.filter_by(userID = userID).first()
            query_data.name = name
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        return jsonify({"rspCode": "200"})          #名稱修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤
        
#設定使用者名稱
@test.route('/setting/userName', methods=['POST'])
def setting_userName():
    if request.method == 'POST':
        userName = request.get_json()['userName']
        userID = request.get_json()['userID']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", userName) == None:
            return jsonify({"rspCode": "401"})      #使用者名稱格式不符
        try:
            query_data = account.query.filter(account.userName == func.binary(userName)).first()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        if query_data:
            return jsonify({"rspCode": "402"})      #使用者名稱重複
        try:
            query_data = account.query.filter_by(userID = userID).first()
            query_data.userName = userName
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        return jsonify({"rspCode": "200"})          #使用者名稱修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤

#設定密碼
@test.route('/setting/userPassword', methods=['POST'])
def setting_userPassword():
    if request.method == 'POST':
        userPassword = request.get_json()['userPassword']
        userOldPassword = request.get_json()['userOldPassword']
        if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", userPassword) == None:
            return jsonify({"rspCode": "401"})      #密碼格式不符
        userID = request.get_json()['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        if not check_same(userOldPassword, query_data.userPassword, query_data.salt):
            return jsonify({"rspCode": "402"})      #舊密碼錯誤
        try:
            salt = generate_salt()
            query_data = account.query.filter_by(userID = userID).first()
            query_data.userPassword = encrypt(userPassword, salt)
            query_data.salt = salt
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        return jsonify({"rspCode": "200"})          #密碼修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤

#設定電子郵件
@test.route('/setting/userMail', methods=['POST'])
def setting_userMail():
    if request.method == 'POST':
        userMail = request.get_json()['userMail']
        userID = request.get_json()['userID']
        if len(userMail) > 50 or len(userMail) < 1:
            return jsonify({"rspCode": "401"})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", user[3]) == None:
            return jsonify({"rspCode": "402"})      #電子郵件格式不符
        try:
            existMail = account.query.filter(account.userMail == func.binary(userMail)).first()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        if existMail:
            if existMail.userID == userID:
                return jsonify({"rspCode": "403"})  #電子郵件並未修改
            else:
                return jsonify({"rspCode": "404"})  #電子郵件已被使用
        try:
            query_data = account.query.filter_by(userID = userID).first()
            query_data.userMail = userMail
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        return jsonify({"rspCode": "200"})          #電子郵件修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤

#設定手機號碼
@test.route('/setting/userPhone', methods=['POST'])
def setting_userPhone():
    if request.method == 'POST':
            userPhone = request.get_json()['userPhone']
            userID = request.get_json()['userID']
            if re.search(r"^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$", userPhone) == None:
                return jsonify({"rspCode": "401"})      #手機號碼格式不符
            try:
                query_data = account.query.filter_by(userID = userID).first()
                query_data.userPhone = userPhone
                db.session.commit()
            except:
                return jsonify({"rspCode": "400"})      #資料庫錯誤
            return jsonify({"rspCode": "200"})          #手機號碼修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤

#設定性別
@test.route('/setting/userGender')
def setting_userGender():
    if request.method == 'POST':
        userGender = request.get_json()['userGender']
        userID = request.get_json()['userID']
        if int(userGender) > 2 or int(userGender) < 0:
            return jsonify({"rspCode": "401"})      #性別異常
        try:
            query_data = account.query.filter_by(userID = userID).first()
            query_data.userGender = userGender
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        return jsonify({"rspCode": "200"})          #性別修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤

#設定生日
@test.route('/setting/userBirthday', methods=['POST'])
def setting_userBirthday():
    if request.method == 'POST':
        userBirthday = request.get_json()['userBirthday']
        userID = request.get_json()['userID']
        if re.search(r"^((18|19|20)[0-9]{2})[-\/.](0?[1-9]|1[012])[-\/.](0?[1-9]|[12][0-9]|3[01])$", userBirthday) == None:
            return jsonify({"rspCode": "401"})       #生日格式不符
        else:
            today = datetime.date.today()
            other_day = datetime.date(int(userBirthday[0:4]), int(userBirthday[5:7]), int(userBirthday[8:10]))
            result = other_day - today
            if result.days > 0:
                return jsonify({"rspCode": "402"})  #未來人錯誤
        try:
            query_data = account.query.filter_by(userID = userID).first()
            query_data.userBirthday = userBirthday
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})      #資料庫錯誤
        return jsonify({"rspCode": "200"})          #名稱修改成功
    else:
        return jsonify({"rspCode": "300"})          #method使用錯誤

#設定個人照片
@test.route('/setting/propic', methods=['POST'])
def setting_propic():
    if request.method == 'POST':
        f = request.files['propic']
        userID = request.values['userID']
        allowExtention = set(['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'])
        if f and f.filename.rsplit('.', 1)[1] in allowExtention:
            path = current_app.config['UPLOAD_FOLDER'] + "/app/static/img/propic/{}.jpg".format(userID)
            f.save(path)
            return redirect(url_for('USER.setting'))
        else:
            print(f.filename)
            return redirect(url_for('USER.setting'))

#取得個人資料
@test.route('/output', methods=['POST'])
def output():
    if request.method == 'POST':
        userID = request.get_json()['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
        except:
            return jsonify({"rspCode": "400", "userID": "", "name": "", "userGender": "", "userAge": "", "userInfo": ""})      #資料庫錯誤
        other_day = transferToDate(query_data.userBirthday)
        userAge = floor((datetime.date.today() - other_day).days/365.25)
        return jsonify({"rspCode": "200", "userID": userID, "name": query_data.name, "userGender": query_data.userGender,\
                        "userAge": userAge, "userInfo": query_data.userInfo})                                                  #成功取得個人資料
    else:
        return jsonify({"rspCode": "300", "userID": "", "name": "", "userGender": "", "userAge": "", "userInfo": ""})          #method使用錯誤

#取得SR歷史的任務
@test.route('/SR/output/record', methods=['POST'])
def SR_output_record():
    if request.method == 'POST':
        userID = request.get_json()['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
            if query_data == None:
                return jsonify({"rspCode": "401", "taskRecord": ""})                                              #userID錯誤
        except:
            return jsonify({"rspCode": "400", "taskRecord": ""})                                                  #資料庫錯誤
        taskRecord = []
        for task in query_data.taskSR:
            if task.taskStatus not in [0, 1, 2]:
                taskRecord.append(task)
        sortTask(taskRecord, 0, len(taskRecord) - 1)
        taskRecordJson = []
        for task in taskRecord:
            taskRecordJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                    "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                    "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                    "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name})
        return jsonify({"rspCode": "200", "taskRecord": taskRecordJson})                        #成功取得
    else:
        return jsonify({"rspCode": "300", "taskRecord": ""})                                        #method使用錯誤

#取得SP已通過的任務
@test.route('/SP/output/passed', methods=['POST'])
def SP_output_passed():
    if request.method == 'POST':
        userID = request.get_json()['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
            if query_data == None:
                return jsonify({"rspCode": "401", "taskPassed": ""})                                              #userID錯誤
        except:
            return jsonify({"rspCode": "400", "taskPassed": ""})                                                  #資料庫錯誤
        taskPassed = []
        for task in query_data.taskSP:
            if task.taskStatus == 2:
                taskPassed.append(task)
        sortTask(taskPassed, 0, len(taskPassed) - 1)
        taskPassedJson = []
        for task in taskPassed:
            taskPassedJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                    "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                    "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                    "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name})
        return jsonify({"rspCode": "200", "taskPassed": taskPassedJson})                                        #成功取得
    else:
        return jsonify({"rspCode": "300", "taskPassed": ""})                                                    #method使用錯誤

#取得SP審核中的任務
@test.route('/SP/output/checking', methods=['POST'])
def SP_output_checking():
    if request.method == 'POST':
        userID = request.get_json()['userID']
        try:
            query_data = taskCandidate.query.filter_by(userID = userID).order_by(taskCandidate.taskID).all()
            if query_data == None:
                return jsonify({"rspCode": "401", "taskChecking": ""})                                              #userID錯誤
        except:
            return jsonify({"rspCode": "400", "taskChecking": ""})                                                  #資料庫錯誤
        taskChecking = []
        for candidate in query_data:
            print(candidate.task.taskStatus)
            if candidate.task.taskStatus == 1:
                taskChecking.append(candidate.task)
        sortTask(taskChecking, 0, len(taskChecking) - 1)
        taskCheckingJson = []
        for task in taskChecking:
            taskCheckingJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                    "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                    "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                    "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name})
        return jsonify({"rpsCode": "200", "taskChecking": taskCheckingJson})                                        #成功取得
    else:
        return jsonify({"rspCode": "300", "taskChecking": ""})                                                      #method使用錯誤

#取得SP遭拒絕的任務
@test.route('/SP/output/refused', methods=['POST'])
def SP_output_refused():
    if request.method == 'POST':
        userID = request.get_json()['userID']
        try:
            query_data = taskCandidate.query.filter_by(userID = userID).order_by(taskCandidate.taskID).all()
            if query_data == None:
                return jsonify({"rspCode": "401", "taskRefused": ""})                                              #userID錯誤
        except:
            return jsonify({"rspCode": "400", "taskRefused": ""})                                                  #資料庫錯誤
        taskRefused = []
        for candidate in query_data:
            if candidate.task.taskStatus >= 2 and candidate.task.SP[0].userID != userID:
                taskRefused.append(candidate.task)
        sortTask(taskRefused, 0, len(taskRefused) - 1)
        taskRefusedJson = []
        for task in taskRefused:
            taskRefusedJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                    "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                    "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                    "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name})
        return jsonify({"rpsCode": "200", "taskRefused": taskRefusedJson})                                        #成功取得
    else:
        return jsonify({"rspCode": "300", "taskRefused": ""})                                                     #method使用錯誤

#取得SP歷史的任務
@test.route('/SP/output/record', methods=['POST'])
def SP_output_record():
    if request.method == 'POST':
        userID = request.get_json()['userID']
        try:
            query_data = taskCandidate.query.filter_by(userID = userID).order_by(taskCandidate.taskID).all()
            if query_data == None:
                return jsonify({"rspCode": "401", "taskRefused": ""})                                              #userID錯誤
        except:
            return jsonify({"rspCode": "400", "taskRefused": ""})                                                  #資料庫錯誤
        taskRecord = []
        for candidate in query_data:
            if candidate.task.taskStatus >= 2 and candidate.task.SP[0].userID == userID:
                taskRecord.append(candidate.task)
        sortTask(taskRecord, 0, len(taskRecord) - 1)
        taskRecordJson = []
        for task in taskRecord:
            taskRecordJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                    "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                    "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                    "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name})
        return jsonify({"rpsCode": "200", "taskRecord": taskRecordJson})                                        #成功取得
    else:
        return jsonify({"rspCode": "300", "taskRecord": ""})                                                     #method使用錯誤

#取得個人頁面已發任務
@test.route('/output/task', methods=['POST'])
def output_task():
    if request.method == 'POST':
        userID = request.get_json()['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
            if query_data == None:
                return jsonify({"rspCode": "401", "taskWaiting": ""})                                              #userID錯誤
        except:
            return jsonify({"rspCode": "400", "taskWaiting": ""})                                                  #資料庫錯誤
        taskWaiting = []
        for task in query_data.taskSR:
            if task.taskStatus in [0, 1]:
                taskWaiting.append(task)
        sortTask(taskWaiting, 0, len(taskWaiting) - 1)
        taskWaitingJson = []
        for task in taskWaiting:
            taskRecordJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskPoint": task.taskPoint,\
                                    "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime)})
        return jsonify({"rspCode": "200", "taskWaiting": taskWaitingJson})                                        #成功取得
    else:
        return jsonify({"rspCode": "300", "taskWaiting": ""})                                                    #method使用錯誤


@test.route('/sql_test')
def sql_test():
    query = adminAccount.query.filter(adminAccount.adminName == 'Tom').first()
    print(query.adminType)

@test.route('/USER/mail', methods=['POST'])
def delete():
    
    return 'ok'

@test.route('/login_USER_page')
def login_USER_page():
    if not (session.get('userID')):
        return render_template('navbarVisitor.html')
    else:
        return redirect('/info/' + session.get('userID'))

@test.route('/register_page')
def register_page():
    return render_template('registerUser.html')

@test.route('/')
def directory():
    return render_template('test/directory.html')

@test.route('/info')
def info():
    userName =session.get('userName') 
    if not userName:   
        return redirect(url_for('login_USER_page'))
    else:
        return render_template('test/directory.html', welcome = '歡迎' + userName)

@test.route('/upload_js_page')
def upload_js_page():
    return render_template('test/upload_js.html')

@test.route('/upload_html_page')
def upload_html_page():
    return render_template('test/upload_html.html')

@test.route('/upload_css_page')
def upload_css_page():
    return render_template('test/upload_css.html')

@test.route('/upload_img_page')
def upload_img_page():
    return render_template('test/upload_img.html')

@test.route('/forget_password_page')
def forget_password_page():
    return render_template('forgotPasswordUser.html')

@test.route('/USER/reset_password_page/<token>')
def reset_password_page(token):
    print(token)
    if validate_token(current_app.config['SECRET_KEY'], token):
        return render_template('resetPassword.html')
    else:
        return "該網頁已過期"


######################################################

#入口網站資訊
#網站介紹上傳
#用json傳intro
#回傳rspCode
@test.route('/upload_web_intro', methods = ['POST'])
def upload_web_intro():
    if request.method == 'POST':    
       #寫在webIntro.txt
       file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'webIntro.txt' , 'w')
       #目前預設傳來的資訊叫intro
       #且直接是str
       json = request.get_json()
       intro = json['intro']  
       if file.write(intro):
           file.close()
           return jsonify({"rspCode": "200"})
       else:       
           file.close()       
           #rspCode 400 檔案寫入失敗
           return jsonify({"rspCode" : "400"})
    else:
        return jsonify({"rspCode":"300"})
 
#網站介紹顯示
#回傳rspCode,webIntro
@test.route("/output_webIntro", methods = ['GET'])
def output_web_intro():
    if request.method == 'GET':
        #開啟webIntro.txt
        try:
            file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + "webIntro.txt", 'r')
        except:
            #rspCode 400:webIntro.txt開啟失敗
            return jsonify({"rspCode" : "400","webIntro":''})
        intro = jsonify({"rspCode":"200","webIntro":file.read()})
        file.close()
        return intro
    else:
        return jsonify({"repCode":"300","webIntro":''})    

#最新資訊資訊上傳   
#用form傳title,content,file(jpg,jpeg,png)
@test.route('/upload_news', methods = ['POST'])
def upload_news():
    if request.method == 'POST':
        #目前預設傳來的資訊叫content,title,file
        #且文字直接是str
        title = request.values['title']
        content = request.values['content'] 
        fileImage = request.files['file']
        #檢查values是否為空
        if title == '' or content == '' or fileImage.filename == '':
            #rspCode 400:標題,內文,圖片有空值
            return jsonify({"rspCode" : "400"})
        #檢查tittle有沒有太大
        if len(title) > 30:
            #rspCode 405:title太長
            return ({"rspCode":"405"})
        time = str(datetime.datetime.now()).rsplit('.',1)[0]
        try:
            db.engine.execute(insert_news(title,time))
        except:
            #rspCode 404:標題上傳錯誤
            return jsonify({"rspCode":"404"})
        #目前預設傳來的圖片叫做file,允許jpg,gpeg,png
        #檢查fileImage
        if fileImage.mimetype == 'image/jpg' or fileImage.mimetype == 'image/png' or fileImage.mimetype == 'image/jpeg':
            try:
                #設定filename = newsID.jpg
                filename = str(db.engine.execute(max_newsID()).fetchone()[0]) + '.jpg'
                #儲存檔案到指定位置
                fileImage.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage/' , filename))
            except:
                #rspCode 402:圖片上傳錯誤
                return jsonify({"rspCode":"402"})
        else:   
            #rspCode 401:圖片檔名錯誤
            return jsonify({"rspCode" : "401"})
        try:    
            #內文上傳
            fileContentName = str(db.engine.execute(max_newsID()).fetchone()[0]) + '.txt' 
            fileContent = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +  'newsContent/' + fileContentName, 'w')
            fileContent.write(content)
            fileContent.close()
            return jsonify({"rspCode":"200"})
        except:
            file.close()
            #rspCode 403:內文上傳錯誤
            return jsonify({"rspCode":"403"})
    else:
        return jsonify({"repCode":"300"})

#最新資訊圖片顯示
#在網址帶入要顯示的編號
#回傳rspCode,img
@test.route("/output_news_image/<number>", methods = ['GET'])
def output_newsImage(number):
    if request.method == 'GET':
        try:
            if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage' + "/{}.jpg".format(number)):
                filename = number + '.jpg'
                return jsonify({"rspCode": "200", "img": filename})
            else:
                #這個編號沒檔案
                return jsonify({"rspCode":"401","img":""})
        except:
            #圖片檔名獲取錯誤
            return jsonify({"rspCode" : "400","img":""})
    else:
        return jsonify({"rspCode":"300","img":""})

#最新資訊內文顯示
#在網址帶入要顯示的編號
#回傳rspCode,content
@test.route("/output_news_content/<number>", methods = ['GET'])
def output_news_content(number):
    if request.method == 'GET':

        try:
            filename = number + '.txt'
            file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/newsContent/' + filename, 'r')
            content = jsonify({"rspCode": "200","content":file.read()})
            file.close()
            return content
        except:
            #內文顯示錯誤
            return jsonify({"rspCode" : "400","content":""})
    else:
        return jsonify({"rspCode":"300","content":""})
#最新消息標題顯示
#在網址帶入要顯示的編號
#回傳rspCode,title
@test.route("/output_news_title/<number>", methods = ['GET'])
def output_news_title(number):
    if request.method == 'GET':
        try:
            return jsonify({"rspCode":"200","title":db.engine.execute(select_title(number)).fetchone()[0]})
        except:
            #最新消息顯示錯誤
            return jsonify({"rspCode": "400","title":""})
    else:
        return jsonify({"rspCode":"300","title":""})
#編輯最新消息
#在網址帶入要編輯的編號
#用form傳file(jpg,png,jpeg),title,content
#回傳rspCode
@test.route("/edit_news/<number>", methods = ['POST'])
def edit_news(number):
    if request.method == 'POST':
        #目前預設傳來的圖片叫做file
        fileImage = request.files['file']
        title = request.values['title']
        content = request.values['content']
        if len(title) > 30:
            #rspCode 404:title太長
            return jsonify({"rspCode":"404"})
        if fileImage.filename != '':
            #允許jpg,jpeg,png
            if fileImage.mimetype == 'image/jpg' or fileImage.mimetype == 'image/png' or fileImage.mimetype == 'image/jpeg':
                try:
                    #設定filename = newsID.jpg
                    filename = number + '.jpg'
                    #儲存檔案到指定位置
                    os.remove(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage' + "/" + filename)
                    fileImage.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +'newsImage', filename))
                except:
                    #rspCode 401:圖片更新失敗
                    return jsonify({"rspCode":"401"})
            else:
                #rspCode 400:圖片檔名錯誤
                return jsonify({"rspCode" : "400"})
        if title != '':
            try:
               if db.engine.execute(select_title(number)).fetchone() != None:
                    db.engine.execute(update_title(title,number))
               else:
                    return jsonify({"rspCode":"402"})
            except:
                #rspCode 402:標題更新失敗
                return jsonify({"rspCode":"402"})
        if content != '':
            try:
                if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + "newsContent/{}.txt".format(number)):
                    file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + "newsContent/{}.txt".format(number),'w')
                    file.write(content)
                    file.close()
                else:
                    return jsonify({"rspCode":"403"})
            except:
                #rspCode 403:內文更新失敗
                return jsonify({"rspCode":"403"})
        return jsonify({"rspCode":"200"})
    else:
        return jsonify({"rspCode":"300"})
        
#刪除最新消息
#在網址帶上要刪除的編號
#回傳rspCode
@test.route("/delete_news/<number>", methods = ['POST'])
def delete_news(number):
    if request.method == 'POST':
        #刪除資料庫中資料
        try:
            if db.engine.execute(select_title(number)).fetchone()[0] != None:
                db.engine.execute(delete_news_(number))
            else:
                #rspCode 400:資料庫資料刪除失敗
                return jsonify({"rspCode" : "400"})
        except: 
            #rspCode 400:資料庫資料刪除失敗
            return jsonify({"rspCode" : "400"})
        #刪除伺服器中檔案
        if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage' + "/{}.jpg".format(number)):
            newsImage = current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +'newsImage' + "/{}.jpg".format(number)
        else:
            #rspCode 401:圖片檔案不存在
            return jsonify({"rspCode" : "401"})
        newsContent = current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile' + "/newsContent/{}.txt".format(number)
        try:
            os.remove(newsImage)
        except:
            #rspCode 402:圖片刪除失敗
            return jsonify({"rspCode" : "402"})
        try:
            os.remove(newsContent)
            return jsonify({"rspCode" : "200"})
        except:
            #rspCode 403:內文刪除失敗
            return jsonify({"rspCode" : "403"})
    else:
        return jsonify({"rspCode":"300"})

#顯示現在有的newsID
#回傳 rspCode 、 number
@test.route("/useful_numbers", methods = ['GET'])
def useful_numbers():
    if request.method != "GET":
        return jsonify({"rspCode":"300","numberList":"","max":""})
    try:
        number_list = []
        number = db.session.query(news.newsID).all()
        for num in number:
            number_list.append(num[0])
        return jsonify({"rspCode":"200","numberList":number_list,"max":number_list[len(number_list)-1]})
    except:
        return jsonify({"rspCode":"400","numberList":"","max":""})

    #前往更新入口網站
@test.route("/SA/updateWeb")
def updateWebSA():
    return render_template("updateWebSA.html")

@test.route("/AU/updateWeb")
def updateWebAU():
    return render_template("updateWebAU.html")
 
#點數申請相關
#更新申請對象
#要json傳groupName
#回傳rspCpde
@test.route('/update_apply_group', methods = ['POST'])
def update_apply_group():
    if request.method == 'POST':
        try:
            json = request.get_json()
            groupName = json['groupName']
            file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +'/group_name.txt','w')
            file.write(groupName)
            file.close()
            return jsonify({"rspCode":"200"})
        except:
            #rspCode 400:申請對象寫入失敗
            return jsonify({"rspCode":"400"})
    else:
        return jsonify({"rspCode":"300"})
#顯示申請對象
#回復rspCode,groupName
@test.route('/output_apply_group', methods = ['GET'])
def output_apply_group():
    if request.method == "GET":
        try:
            file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile' + '/group_name.txt','r')
            groupName = file.read()
            file.close()
            return jsonify({"rspCode":"200","groupName":groupName})
        except:
            #rspCode 400:檔案讀取失敗
            return jsonify({"rspCode":"400","groupName":""})
    else:
        return jsonify({"rspCode":"300","groupName":""})


#顯示可申請類別
#回復rspCode,allClass
@test.route("/output_apply_class" ,methods = ['GET'])
def output_apply_class():
    if request.method == 'GET':
        try:
            dbClassData = db.engine.execute(list_alive_apply_class()).fetchall()
            allClass = []
            for object in dbClassData:
                allClass.append(object[0])
            return jsonify({"rspCode":"200","allClass":allClass})
        except:
            #rspCode 400:顯示失敗
            return jsonify({"rspCode":"400","allClass":""})
    else:
        return jsonify({"rspCode":"300","allClass":""})
 
#刪除申請類別
#要json輸入className
#回傳rspCode
@test.route("/delete_apply_class", methods = ['POST'])
def delete_apply_class():
    if request.method == 'POST':
        try:
            json = request.get_json()
            deleteClassName = json['class']
            db.engine.execute(let_apply_condition_die(deleteClassName))
            return jsonify({"rspCode":"200"})
        except:
            #rspCode 400:刪除失敗
            return jsonify({"rspCode":"400"})
    else:
        return jsonify({"rspCode":"300"})
#更新申請文件
#要form傳file(pdf)
#回傳rspCode
@test.route("/upload_apply_condition_pdf" ,methods = ['POST'])
def upload_apply_condition_pdf():
    if request.method == 'POST':
        #目前預設傳來的東西叫做file,允許pdf
        try:
            filePdf = request.files['file']
        except:
            #檔案傳輸方式錯誤、或是檔案超過2MB
            return jsonify({"rspCode":"402"})
        #檢查fileImage
        if filePdf.mimetype == 'application/pdf':
            try:
                #儲存檔案到指定位置
                filePdf.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile' , 'apply_condition.pdf'))
                return jsonify({"rspCode":"200"})
            except:
                #rspCode 400:圖片上傳錯誤
                return jsonify({"rspCode":"400"})
        else:
            #檔案類型或名稱不許可
            return jsonify({"rspCode":"401"})
    else:
        return jsonify({"rspCode":"300"})
#回傳申請文件名
#回傳rspCode,fileName
@test.route("/output_apply_condition_pdf", methods = ['GET'])
def ouput_apply_condition_pdf():
    if request.method == 'GET':
        #try:
            
            if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/'+'apply_condition.pdf'):
                return jsonify({"rspCode":"200","fileName":"apply_condition.pdf"})
            else:
                #檔案不存在
                return jsonify({"rspCode":"401","fileName":""})
        #except:
            #rspCode 400:回傳失敗
            return jsonify({"rspCode":"400","fileName":""})
    else:
        return jsonify({"repCode":"300"})

#新增與更新
#要json傳class,once,one,three,six,year(後面幾個是quota,0為移除)
#回傳rspCode,notAllow
@test.route('/update_add_apply_quota' ,methods = ['POST'])
def update_add_apply_quota():
    try:
        if request.method == 'POST':
            json = request.get_json()
            notAllow = []
            className = json['class']
            once = json['once']
            one = json['one']
            three = json['three']
            six = json['six']
            year = json['year']
            #檢查輸入
            if className == '' or className == '其他':
                notAllow.append("class")
            if once.isdigit() == False:
                notAllow.append("once")
            elif int(once) < 0:
                notAllow.append("once")
            elif len(once) > 5:
                notAllow.append("once")
            if one.isdigit() == False:
                notAllow.append("one")
            elif int(one) < 0:
                notAllow.append("one")
            elif len(one) > 5:
                notAllow.append("one")
            if three.isdigit() == False:
                notAllow.append("three")
            elif int(three) < 0:
                notAllow.append("three")
            elif len(three) > 5:
                notAllow.append("three")
            if six.isdigit() == False:
                notAllow.append("six")
            elif int(six) < 0:
                notAllow.append("six")
            elif len(six) > 5:
                notAllow.append("six")
            if year.isdigit() == False:
                notAllow.append("year")
            elif int(year) < 0:
                notAllow.append("year")
            elif len(year) > 5:
                notAllow.append("year")
            if notAllow != []:
                #rspCode 401:輸入不合法
                return jsonify({"rspCode":"401","notAllow":notAllow})
            #一次性
            #檢查是不是0
            if once != '0':
                #檢查原本有沒有這種一次性
                if db.engine.execute(show_quota_by_period_class_alive(className,0)).fetchone() != None:
                    #檢查和已有的once一不一樣，一樣的話不做事
                    if int(once) != db.engine.execute(show_quota_by_period_class_alive(className,0)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_class_period(className,0))
                        db.engine.execute(add_apply_condition(0,className,int(once)))                    
                else:
                    db.engine.execute(add_apply_condition(0,className,int(once)))
            else:
                #檢查有沒有這種一次性
                if db.engine.execute(show_quota_by_period_class_alive(className,0)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_class_period(className,0))
            #一個月
            if one != '0':
                if db.engine.execute(show_quota_by_period_class_alive(className,30)).fetchone() != None:
                    if int(one) != db.engine.execute(show_quota_by_period_class_alive(className,30)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_class_period(className,30))
                        db.engine.execute(add_apply_condition(30,className,int(one)))                    
                else:
                    db.engine.execute(add_apply_condition(30,className,int(one)))
            else:
                if db.engine.execute(show_quota_by_period_class_alive(className,30)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_class_period(className,30))
            #三個月
            if three != '0':
                if db.engine.execute(show_quota_by_period_class_alive(className,90)).fetchone() != None:
                    if int(three) != db.engine.execute(show_quota_by_period_class_alive(className,90)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_class_period(className,90))
                        db.engine.execute(add_apply_condition(90,className,int(three)))                    
                else:
                    db.engine.execute(add_apply_condition(90,className,int(three)))
            else:
                if db.engine.execute(show_quota_by_period_class_alive(className,90)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_class_period(className,90))
            #六個月
            if six != '0':
                if db.engine.execute(show_quota_by_period_class_alive(className,180)).fetchone() != None:
                    if int(six) != db.engine.execute(show_quota_by_period_class_alive(className,180)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_class_period(className,180))
                        db.engine.execute(add_apply_condition(180,className,int(six)))                    
                else:
                    db.engine.execute(add_apply_condition(180,className,int(six)))
            else:
                if db.engine.execute(show_quota_by_period_class_alive(className,180)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_class_period(className,180))
            #一年
            if year != '0':
                if db.engine.execute(show_quota_by_period_class_alive(className,365)).fetchone() != None:
                    if int(year) != db.engine.execute(show_quota_by_period_class_alive(className,365)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_class_period(className,365))
                        db.engine.execute(add_apply_condition(365,className,int(year)))                    
                else:
                    db.engine.execute(add_apply_condition(365,className,int(year)))
            else:
                if db.engine.execute(show_quota_by_period_class_alive(className,365)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_class_period(className,365))
            return jsonify({"rspCode":"200","notAllow":""})

        else:
            return jsonify({"rspCode":"300","notAllow":""})
    except:
        #rspCode 400:某個地方爆掉但不知道哪裡
        return jsonify({"rspCode":"400","notAllow":""})

#回傳要求的quota和condition id
#要json傳class,period
#回傳rspCode,conditionID,quota
@test.route("/output_quota_conditionID",methods =['GET'])
def output_quota_conditionID():
    if request.method == 'GET':
        try:
            json = request.get_json()   
            if json['class'] == '其他':
                #其他沒id和quota
                return jsonify({"conditionID":"","quota":"","rspCode":"201"})
            elif json['class'] == '' or json['period'] == '':
                #class或period未填
                return jsonify({"conditionID":"","quota":"","rspCode":"400"})
            dbData = db.engine.execute(show_quota_conditionID_by_class_period(json['class'],json['period'])).fetchone()
            if dbData != None:
                return jsonify({"conditionID":str(dbData[0]),"quota":str(dbData[1]),"rspCode":"200"})
            else:
                #rspCode 402:沒有此資料
                return jsonify({"conditionID":"","quota":"","rspCode":"402"})
        except:
            #抓取資料失敗
            return jsonify({"conditionID":"","quota":"","rspCode":"401"})
    else:
        return jsonify({"conditionID":"","quota":"","rspCode":"300"})

#根據所選的class回復period
#要json傳class
#回傳rspCode,periodList
@test.route("/output_allow_period", methods = ['GET'])
def return_period_by_class():
    try:
        if request.method == 'GET':
            json = request.get_json()
            className = json['class']
            if className == '其他':
                return jsonify({"periodList":"0,30,90,180,365","quotaList":"","rspCode":"200"})
            else:
                dbData = db.engine.execute(out_put_allow_period(className)).fetchall()
                quotaList = []
                periodList = []
                conditionIDList = []
                if dbData != []:
                    for period in dbData:
                        dbData2 = db.engine.execute(show_quota_conditionID_by_class_period(className,period[0])).fetchone()
                        periodList.append(str(period[0]))
                        quotaList.append(dbData2[1])
                    return jsonify({"periodList":periodList,"quotaList":quotaList,"rspCoide":"200"})
                else:
                    #rspCode 201:此class沒有可被申請的週期
                    return jsonify({"periodList":"","quotaList":"","rspCoide":"201"})
        else:
            return jsonify({"periodList":"","quotaList":"","rspCode":"300"})
    except:
            #rspCode 400:某個地方爆掉
            return jsonify({"periodList":"","rspCode":"400"})

#前往更新申請條件 AA
@test.route("/AA/updateCondition")
def updateConditionAA():
    return render_template("updateConditionAA.html")

#前往更新申請條件 SA
@test.route("/SA/updateCondition")
def updateConditionSA():
    return render_template("updateConditionSA.html")

#使用者新增申請
#要form傳frequency,period,result,class,quota,file(pdf)
#回傳rspCode,notAllow
@test.route("/USER/add_apply", methods = ['POST'])
def user_add_apply():
    try:
        if request.method == 'POST':
            notAllow = []
            userID = session.get('userID')
            userID = 1
            time = str(datetime.datetime.now()).rsplit('.',1)[0]
            #檢查各變數與檔案
            if request.values['frequency'].isdigit():
                if int(request.values['frequency']) > 0 and len(request.values['frequency']) < 6:
                    frequency = int(request.values['frequency'])
                else:
                    frequency = 0
                    notAllow.append('frequency')
            else:
                frequency = 0
                notAllow.append('frequency')
            if request.values['period'] in ['0','30','90','180','365']:
                    restTime = int(request.values['period']) * frequency
                    nextTime = int(request.values['period'])
            else:
                notAllow.append('period')
            result = request.values['result']        
            if(request.values['class'] != '其他'):
                try:
                    if notAllow != []:
                        #rspCode 403:有輸入不符合格式
                        return jsonify({"notAllow":notAllow,"rdpCode":"403"})
                    conditionID = db.engine.execute(show_conditionID(request.values['class'],request.values['period'])).fetchone()[0]
                except:
                    #rspCode 401:找不到conditionID
                    return jsonify({"rspCode":"401","notALlow":""})
            else:
                if result == '':
                    #rspCode 402:其他要填原因
                    return jsonify({"rspCode":"402","notALlow":""})
                #檢查其他的quota
                if request.values['quota'].isdigit():
                    if int(request.values['quota']) > 0 and len(request.values['quota']) < 6:
                        quota = request.values['quota']
                    else:
                        notAllow.append('quota')
                else:
                    notAllow.append('quota')
                if notAllow != []:
                    #rspCode 403:有輸入不符合格式
                    return jsonify({"notAllow":notAllow,"rdpCode":"403"})
                #檢查有沒有一樣的其他了
                if db.engine.execute(find_other_apply_condition_id(nextTime,quota)).fetchone() != None:
                    conditionID = db.engine.execute(find_other_apply_condition_id(nextTime,quota)).fetchone()[0]
                #沒有才建新的
                else:
                    db.engine.execute(set_up_apply_condition('其他',nextTime,quota))
                    conditionID = db.engine.execute(find_other_apply_condition_id(nextTime,quota)).fetchone()[0]     
            file = request.files['file']
            #建立apply
            db.engine.execute(add_apply(frequency,restTime,nextTime,userID,conditionID,result,time))   
            #檢查有沒有傳檔案
            if file.filename != "":
                try:
                    #檢查fileName
                    if file.mimetype == 'application/pdf':
                        originFileName = '{}'.format(file.filename)
                        num = str(db.engine.execute(find_max_applyId_by_user_ID(userID)).fetchone()[0])
                        os.makedirs(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}'.format(num))
                        fileTxt =open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}/{}.txt'.format(num,num),'w',encoding="utf-8")
                        fileTxt.write(file.filename)
                        fileTxt.close()
                        #儲存檔案到指定位置
                        filename = '{}.pdf'.format(num)
                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}'.format(num),filename))
                except:
                    #rspCode 404:pdf上傳錯誤
                    return jsonify({"rspCode":"404","notALlow":""})
  
            return jsonify({"rspCode":"200","notALlow":""})
        else:
            return jsonify({"rspCode":"300","notALlow":""})
    except:
        #rspCode 400:某個地方爆掉但不知道哪裡
        jsonify({"rspCode":"400","notALlow":""})


#審核申請資料顯示
#要json傳(userName,name)(搜尋目標，沒有就傳空值)
#回傳rspCode, userName, userSRRate, userSPRate, applyPdfName, applyID,
#applyClass, applyQuota, applyPeriod, applyFrequency, applyTime, applyResult,
#userID
@test.route('/show_apply_status_0/', methods = ['GET'])
def show_apply_status_0():
    if request.method == 'GET':
        json = request.get_json()
        #搜尋目標
        target = json['name']
        userID = []
        userName = []   
        userSRRate = []
        userSPRate = []
        applyPdfName = []
        applyID = []
        applyClass = []
        applyQuota = []
        applyPeriod = []
        applyFrequency = []
        applyTime = []  
        applyResult = []
        if target == '':
            #`applyID`,`userID`,`conditionID`,`applyTime`,`result`,`frequency`
            applyData = db.engine.execute(get_all_apply_status_0()).fetchall()
        elif len(target) > 20:
            #target不符合
            return jsonify({"rspCode":"401"})
        else:
            #`applyID`,`userID`,`conditionID`,`applyTime`,`result`,`frequency`
            applyData = db.engine.execute(get_all_apply_status_0_search_user_name(target)).fetchall()
           
        try:
           for oneData in applyData:
               
               #`userName`,`SRRate`,SRRateTimes,`SPRate`,SPRateTimes`
               userID.append(oneData[1])
               userData = db.engine.execute(get_apply_judge_user_info(oneData[1])).fetchone()
               userName.append(userData[0])
               try:
                    userSRRate.append(float(userData[1]) / float(userData[2]))
               except:
                    userSRRate.append(None)
               try:
                    userSPRate.append(float(userData[3]) / float(userData[4]))
               except:
                    userSPRate.append(None)
               try:
                    fileTxt =open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}/{}.txt'.format(oneData[0],oneData[0]),'r',encoding="utf-8")   
                    applyPdfName.append(fileTxt.read().split('"')[0])
               except:
                  applyPdfName.append(None)
               applyID.append(oneData[0])
               #`period`,`class`,`quota`
               conditionData = db.engine.execute(show_condition_data(oneData[2])).fetchone()
               applyClass.append(conditionData[1])
               applyQuota.append(conditionData[2])
               applyPeriod.append(conditionData[0])
               applyFrequency.append(oneData[5])
               applyTime.append(oneData[3])
               applyResult.append(oneData[4])
           return jsonify({"rspCode":"200","name":userName,"userSRRate":userSRRate,"userSPRate":userSPRate,"applyPdfName":applyPdfName,"applyID":applyID,"applyClass":applyClass,"applyQuota":applyQuota,"applyPeriod":applyPeriod,"applyFrequency":applyFrequency,"applyTime":applyTime,"applyResult":applyResult,"userID":userID})
        except:
            #rspCode 400:以防萬一
            return jsonify({"rspCode":"400","name":"","userSRRate":"","userSPRate":"","applyPdfName":"","applyID":"","applyClass":"","applyQuota":"","applyPeriod":"","applyFrequency":"","applyTime":"","applyResult":"","userID":""})
        
    else:
            return jsonify({"rspCode":"300","name":"","userSRRate":"","userSPRate":"","applyPdfName":"","applyID":"","applyClass":"","applyQuota":"","applyPeriod":"","applyFrequency":"","applyTime":"","applyResult":"","userID":""})

#審核申請頁面中的簡略紀錄
#要json傳applyID
#回傳rspCode, applyTime, frequency, result, status, judgeTime, period, className,
#quota, oldQuota, applyPdfName, applyID, userID, userName
@test.route('/simple_personal_apply_history/',methods =['GET'])
def simple_personal_apply_history():
    if request.method != 'GET':
        return jsonify({"rspCode":"300","applyTime":"","frequency":"","result":"","status":"","judgeTime":"","period":"","className":"","quota":"","oldQuota":"","applyPdfName":"","applyID":"","userID":"","name":""})
    json = request.get_json()
    applyID = json['applyID']
    if applyID =="":
         #rspCode 400:applyID不存在
        return jsonify({"rspCode":"400","applyTime":"","frequency":"","result":"","status":"","judgeTime":"","period":"","className":"","quota":"","oldQuota":"","applyPdfName":"","applyID":"","userID":"","name":""})
    if db.engine.execute(get_userID_by_applyID(applyID)).fetchone() == None:
        #rspCode 400:applyID不存在
        return jsonify({"rspCode":"400","applyTime":"","frequency":"","result":"","status":"","judgeTime":"","period":"","className":"","quota":"","oldQuota":"","applyPdfName":"","applyID":"","userID":"","name":""})
    userID = db.engine.execute(get_userID_by_applyID(applyID)).fetchone()[0]
    userName = db.engine.execute(select_user_name(userID)).fetchone()[0]
    #conditionID
    #,applyTime,frequency,result,applyStatus,oldConditionID,judgeTime,applyID
    dbApplyData = db.engine.execute(find_all_judged_apply_by_userID(userID,applyID)).fetchall()
    applyTime = []
    judgeTime = []
    result = []
    frequency = []
    status = []
    quota = []
    period = []
    className = []
    oldQuota = []
    applyPdfName = []
    historyApplyID = []
    for apply in dbApplyData:
        #`period`,`class`,`quota` 
        condition = db.engine.execute(show_old_condition_data(apply[0])).fetchone()
        applyTime.append(apply[1])
        frequency.append(apply[2])
        result.append(apply[3])
        status.append(apply[4])
        judgeTime.append(apply[6])
        period.append(condition[0])
        className.append(condition[1])
        if apply[4] == 1:
            quota.append(condition[2])
        else:
            quota.append(0)
        historyApplyID.append(apply[7])
        try:
            fileTxt =open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}/{}.txt'.format(apply[7],apply[7]),'r',encoding="utf-8")
            applyPdfName.append(fileTxt.read().split('"')[0])
        except:
            applyPdfName.append(None)
        if apply[5] != None:
            oldQuota.append(db.engine.execute(select_quota_by_conditionID(apply[5])).fetchone()[0])
        else:
            oldQuota.append(condition[2])
    return jsonify({"rspCode":"200","applyTime":applyTime,"frequency":frequency,"result":result,"status":status,"judgeTime":judgeTime,"period":period,"className":className,"quota":quota,"oldQuota":oldQuota,"applyPdfName":applyPdfName,"applyID":historyApplyID,"userID":userID,"name":userName})

#申請附件下載
#要json傳applyID
#回傳 rspCode
@test.route('/apply_pdf_download', methods = ['GET'])
def apply_pdf_download():
    if request.method != 'GET':
        return jsonify({"rspCode":"300"})
    try:
        json = request.get_json()
        applyID = json['applyID']
        filename = os.listdir(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}'.format(applyID))[1]
        send_from_directory(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}'.format(applyID),filename,as_attachment=True)
        return jsonify({"rspCode":"200"})
    except:
        #rspCode 400:檔案不存在
        return jsonify({"rspCode":"400"})

#決定申請是否通過
#要json傳 applyID,applyStatus(案的是核准就給1沒過給2),quotaChange(核准額度有變給值，沒有傳空)
#回傳 rspCode,notAllow
@test.route('/apply_judge', methods = ['POST'])
def apply_judge():
    if request.method != 'POST':
        return jsonify({"rspCode":"300"})
    json = request.get_json()
    applyID = json['applyID']
    applyStatus = json['applyStatus']
    quotaChange = json['quotaChange']
    notAllow = []
    adminID = session.get('adminID')
    adminID = 4
    judgeTime = str(datetime.datetime.now()).rsplit('.',1)[0]
    #檢查ID 和 status
    if applyID == "":
        notAllow.append('applyID')
    elif db.engine.execute(get_conditionID(applyID)).fetchone() == None:
        notAllow.append('applyID')
    if not(applyStatus == '1' or applyStatus == '2'):
        notAllow.append('applyStatus')
    if quotaChange == '':
        if notAllow != []:
            #rspCode 400:有非法輸入
            return jsonify({"rspCode":"400","notAllow":notAllow})
        db.engine.execute(alter_apply_status(applyStatus,applyID))
        userID = db.engine.execute(get_userID_by_applyID(applyID)).fetchone()[0]
        userPoint = db.engine.execute(get_user_point(userID)).fetchone()[0]
        ConditionID = db.engine.execute(get_conditionID(applyID)).fetchone()[0]
        conditionData = db.engine.execute(show_old_condition_data(ConditionID)).fetchone()
        quota = conditionData[2]
        period = conditionData[0]
        plus = userPoint + int(quota)
        if period != 0:
            rest = db.engine.execute(show_rest_time_by_applyID(applyID)).fetchone()[0]
            db.engine.execute(alter_apply_rest_time(applyID,rest))
        db.engine.execute(plus_user_point(plus,userID))
        for x in range(quota):
            pointID = make_point()+"_{}".format(str(db.session.query(point).count()))
            db.engine.execute(make_point_sql(pointID,adminID,userID))
    else:
        #有輸入新的quota才檢查quota
        if not(quotaChange.isdigit()):
            notAllow.append('quotaChange')
        elif int(quotaChange) <= 0:
            notAllow.append('quotaChange')
        if notAllow != []:
            #rspCode 400:有非法輸入
            return jsonify({"rspCode":"400","notAllow":notAllow})
        if applyStatus == '1':
            #status是1就改變apply的condditionID和status
            oldConditionID = db.engine.execute(get_conditionID(applyID)).fetchone()[0]
            conditionData = db.engine.execute(show_old_condition_data(oldConditionID)).fetchone()
            className = conditionData[1]
            period = conditionData[0]
            if db.engine.execute(find_special_apply_condition(className,period,quotaChange)).fetchone() == None:
                newConditionID = db.engine.execute(set_up_special_apply_condition(className,period,quotaChange)).fetchone()[0]
            else:
                newConditionID = db.engine.execute(find_special_apply_condition(className,period,quotaChange)).fetchone()[0]
            db.engine.execute(alter_oldConditionID(oldConditionID,applyID))
            db.engine.execute(alter_conditionID_in_apply(newConditionID,applyID))
            db.engine.execute(alter_apply_status(applyStatus,applyID))

            userID = db.engine.execute(get_userID_by_applyID(applyID)).fetchone()[0]
            userPoint = db.engine.execute(get_user_point(userID)).fetchone()[0]
            plus = userPoint + int(conditionData[2])
            if period != 0:
                rest = db.engine.execute(show_rest_time_by_applyID(applyID)).fetchone()[0]
                db.engine.execute(alter_apply_rest_time(applyID,rest))
            for x in range(quota):
                pointID = make_point()+"_{}".format(str(db.session.query(point).count()))
                db.engine.execute(make_point_sql(pointID,adminID,userID))
        else:
            #不是1就只改status和adminID
            db.engine.execute(alter_apply_status(applyStatus,applyID))

    db.engine.execute(upudate_adminID_in_apply(adminID,applyID))
    db.engine.execute(update_judge_time_in_apply(judgeTime,applyID))
    return jsonify({"rspCode":"200","notAllow":""})


#核准紀錄
#要json傳Name(用來搜尋userName和name),class,period,status，以上四個是搜尋條件，沒有就傳空值
#回傳rspCode, userID, userSRRate, userSPRate, userName, applyPdfName, applyID,
#className, quota, oldQuota, applyTime, judgeTime, period, applyResult,
#applyStatus, applyFrequency
@test.route('/judgement_history', methods = ['GET'])
def judgement_history():
    if request.method != 'GET':
        return jsonify({"rspCode":"300","userID":"","userSRRate":"","userSPRate":"","name":"","applyPdfName":"","applyID":"","className":"","quota":"","oldQuota":"","applyTime":"","judgeTime":"","period":"","applyResult":"","applyStatus":"","applyFrequency":""})
    try:
        userID = []
        userSRRate = []
        userSPRate = []
        userName = []
        applyPdf = []
        applyID = []
        applyClass = []
        applyQuota = []
        oldQuota = []
        applyTime = []
        judgeTime = []
        applyPeriod = []
        result = []
        applyStatus = []
        applyPdfName = []
        frequency = []
        json = request.get_json()
        Name = json['name']
        className = json['class']
        period = json['period']
        status = json['status']
        #conditionID
        #,applyTime,frequency,result,applyStatus,oldConditionID,judgeTime,applyID,userID
        applyData = db.engine.execute(show_judge_history(Name,className,period,status)).fetchall()
        for apply in applyData:
            applyStatus.append(apply[4])
            #`period`,`class`,`quota`
            condition = db.engine.execute(show_condition_data(apply[0])).fetchone()
            applyPeriod.append(condition[0])
            applyClass.append(condition[1])
            if apply[4] == 1:
                applyQuota.append(condition[2])
            else:
                applyQuota.append(0)
            applyTime.append(apply[1])
            frequency.append(apply[2])
            result.append(apply[3])
            if apply[5] != None:
                oldQuota.append(db.engine.execute(show_old_condition_data(apply[5])).fetchone()[2])
            else:
                oldQuota.append(condition[2])
            judgeTime.append(apply[6])
            applyID.append(apply[7])
            try:
                fileTxt =open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}/{}.txt'.format(apply[7],apply[7]),'r',encoding="utf-8")
                applyPdfName.append(fileTxt.read().split('"')[0])
            except:
                applyPdfName.append(None)
            userID.append(apply[8])
            #`userName`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes`
            userData = db.engine.execute(get_apply_judge_user_info(apply[8])).fetchone()
            try:
                userSRRate.append(float(userData[1] / float(userData[2])))
            except:
                userSRRate.append(0)
            try:
                userSPRate.append(float(userData[3] / float(userData[4])))
            except:
                userSPRate.append(0)
            userName.append(apply[0])
        return jsonify({"rspCode":"200","userID":userID,"userSRRate":userSRRate,"userSPRate":userSPRate,"name":userName,"applyPdfName":applyPdfName,"applyID":applyID,"className":applyClass,"quota":applyQuota,"oldQuota":oldQuota,"applyTime":applyTime,"judgeTime":judgeTime,"period":applyPeriod,"applyResult":result,"applyStatus":applyStatus,"applyFrequency":frequency})
    except:
        return jsonify({"rspCode":"400","userID":"","userSRRate":"","userSPRate":"","name":"","applyPdfName":"","applyID":"","className":"","quota":"","oldQuota":"","applyTime":"","judgeTime":"","period":"","applyResult":"","applyStatus":"","applyFrequency":""})

#AA-核准紀錄
@test.route('Admin/AA/approveRecord')
def admin_AA_approveRecord():
    return render_template('approveRecordAA.html')

#SA-核准紀錄
@test.route('Admin/SA/approveRecord')
def admin_SA_approveRecord():
    return render_template('approveRecordSA.html')

#AA-核准申請
@test.route('Admin/AA/approveSystem')
def admin_AA_approveSystem():
    return render_template('approveSystem.html')

#SA-核准申請
@test.route('Admin/SA/approveSystem')
def admin_SA_approveSystem():
    return render_template('approveSystem.html')

#顯示user名單
#要json傳target(搜尋目標，沒有就傳空值)
#回傳rspCode, userName, userID, userSRRate, userSPRate
@test.route('/show_user', methods = ['POST'])
def show_user():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","name":"","userID":"","userSRRate":"","userSPRate":""})
    json = request.get_json()
    #搜尋的東西
    target = json['target']
    userID = []
    userSRRate = []
    userSPRate = []
    userName = [] 
    try:
        if target == '':        
            #`userID`,`userName`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes`
            userData = db.engine.execute(select_all_user()).fetchall()     
        else:
            userData = db.engine.execute(select_search_user(target)).fetchall()
    except:
        #rspCode 400:查資料失敗
            return jsonify({"rspCode":"400","name":"","userID":"","userSRRate":"","userSPRate":""})
    
    for user in userData:
        userID.append(user[0])
        userName.append(user[1])
        try:
            userSRRate.append(float(user[2]) / float(user[3]))
        except:
            userSRRate.append(0)
        try:
            userSPRate.append(float(user[4]) / float(user[5]))
        except:
            userSPRate.append(0)
    return jsonify({"rspCode":"200","userID":userID,"name":userName,"userSRRate":userSRRate,"userSPRate":userSPRate})

#配發按鍵
#要json傳kind(one or all), receiver(one時是目標的ID all是搜尋了什麼), period,
#frequency(一次性傳1), quota
#回傳rspCode 和 notAllow
#回傳rspCode 和 notAllow
@test.route("/allotment" , methods = ['POST'])
def alloment():
    json = request.get_json()#GUANPING
    #only all or one
    kind = json['kind']
    #這裡的receiver如果kind不是all請給要配發的userID，all的話請給SA搜尋了什麼
    receiver = json['receiver']
    period = json['period']
    frequency = json['frequency']
    quota = json['quota']
    notAllow = []
    if not(period == '30' or period == '90' or period == '0' or period == '180' or period == '365'):
        notAllow.append("period")
    if not(frequency.isdigit()):
        notAllow.append('frequency')
    elif int(frequency) < 1:
        notAllow.append("frequency")
    elif len(frequency) > 5:
        notAllow.append("frequency")
    if not(quota.isdigit()):
        notAllow.append('quota')
    elif int(quota) < 1:
        notAllow.append("quota")
    elif len(quota) > 5:
        notAllow.append("quota")
    if notAllow != []:
        #rspCode 401:有違法輸入
        return jsonify({"rspCode":"400","notAllow":notAllow})
    allotmentTime = str(datetime.datetime.now()).rsplit('.',1)[0]
    adminID = session.get('adminID')
    #########
    adminID = json['adminID']
    #########
    if kind == 'one':
        if receiver == '':
            #可能是userID不存在或是adminID不存在
            return jsonify({"rspCode":"400","notAllow":"userID"})
        userID = int(receiver)
        try:
            db.engine.execute(add_allotment(userID,frequency,period,quota,adminID,allotmentTime))
            allotmentID = db.engine.execute(find_max_allotmentID_by_adminID(adminID)).fetchone()[0]
            userPoint = db.engine.execute(get_user_point(userID)).fetchone()[0]
            plus = userPoint + int(quota)
            if period != '0':
                rest = db.engine.execute(show_rest_time_by_alomentID(allotmentID)).fetchone()[0]
                db.engine.execute(alter_allotment_rest_time(allotmentID,str(int(rest) - int(period))))
            db.engine.execute(plus_user_point(plus,userID))
            for num in range(int(quota)):
                pointID = make_point()
                while None != db.engine.execute(check_point_ID(pointID)).fetchone():
                    pointID = make_point()
                db.engine.execute(make_point_sql(pointID,adminID,userID))
            return jsonify({"rspCode":"200"})
        except:
            #可能是userID不存在或是adminID不存在
            return jsonify({"rspCode":"400","notAllow":"userID"})
    elif kind == 'all':
        userData = db.engine.execute(select_search_userID(receiver)).fetchall()
        try:
            for user in userData:
                userID = user[0]
                db.engine.execute(add_allotment(userID,frequency,period,quota,adminID,allotmentTime))  
                allotmentID = db.engine.execute(find_max_allotmentID_by_adminID(adminID)).fetchone()[0]
                userPoint = db.engine.execute(get_user_point(userID)).fetchone()[0]
                plus = userPoint + int(quota)
                if period != '0':
                    rest = db.engine.execute(show_rest_time_by_alomentID(allotmentID)).fetchone()[0]
                    db.engine.execute(alter_allotment_rest_time(allotmentID,str(int(rest) - int(period))))
                db.engine.execute(plus_user_point(plus,userID))
                for num in range(int(quota)):
                    pointID = make_point()
                    while None != db.engine.execute(check_point_ID(pointID)).fetchone():
                        pointID = make_point()
                    db.engine.execute(make_point_sql(pointID,adminID,userID))
            return jsonify({"rspCode":"200","notAllow":""})
        except:
            return jsonify({"rspCode":"400","notAllow":"userID or adminID"})
    else:
        #kind錯誤
        return jsonify({"rspCode":"400","notAllow":"kind"})

#簡易個人配發紀錄
#要json傳userID
#回傳rspCode, period, frequency, quota, time
@test.route("/simple_allotment_history", methods = ['POST'])
def simple_allotment_history():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","period":"","frequency":"","quota":"","time":""})
    try:
        json = request.get_json()
        userID = json['userID']
        time = []
        quota = []
        period = []
        frequency = []
        if not(userID.isdigit()):
             return jsonify({"rspCode":"400","period":"","frequency":frequency,"quota":"","time":""})
        #allotmentTime, quota, period, frequency
        allotmentData = db.engine.execute(select_allotment_simple_history_by_userID(userID))
        for allotment in allotmentData:
            time.append(str(allotment[0]))  
            quota.append(allotment[1])
            period.append(allotment[2])
            frequency.append(allotment[3])
        return jsonify({"rspCode":"200","period":period,"frequency":frequency,"quota":quota,"time":time})
    except:
        #以防萬一
        return jsonify({"rspCode":"400","period":"","frequency":frequency,"quota":"","time":""})
    
#主動配發紀錄
#要json傳target(搜尋了什麼，沒有就傳空值)
#回傳rspCode, period, frequency, quota, time, userID, name
#userSRRate, userSPRate
@test.route('/allotment_history', methods = ['POST'])
def allotment_history():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","time":"","quota":"","period":"","frequency":"","userID":"","name":"","userSRRate":"","userSPRate":""})
    try:
        json = request.get_json()
        target = json['target']
        period = []
        frequency = []
        quota = []
        time = []
        userID = []
        userName = []
        userSRRate = []
        userSPRate = []
        #allotmentTime, quota, period, frequency, userID, userName, SRRate,
        #SRRateTimes, SPRate, SPRateTimes
        allotmentData = db.engine.execute(select_allotment_history_by_userID_userName(target,target)).fetchall()
        for allotment in allotmentData:
            time.append(str(allotment[0]))
            quota.append(allotment[1])
            period.append(allotment[2])
            frequency.append(allotment[3])
            userID.append(allotment[4])
            userName.append(allotment[5])
            try:
                userSRRate.append(str(float(allotment[6]) / float(allotment[7])))
            except:
                userSRRate.append(0)
            try:
                userSPRate.append(str(float(allotment[8]) / float(allotment[9])))
            except:
                userSPRate.append(0)
        return jsonify({"rspCode":"200","time":time,"quota":quota,"period":period,"frequency":frequency,"userID":userID,"name":userName,"userSRRate":userSPRate,"userSPRate":userSPRate})
    except:
        #以防萬一
        return jsonify({"rspCode":"400","time":"","quota":"","period":"","frequency":"","userID":"","name":"","userSRRate":"","userSPRate":""})

