
#coding: utf-8
from flask import Blueprint, render_template, session, url_for, jsonify, request, current_app, redirect
import re, datetime, smtplib, random, os
from sqlalchemy.sql import func
from ..models.hash import *
from ..models.token import *
from ..models.model import *
from ..models.mail import *
from ..models import db, userType
from email.mime.text import MIMEText

Account = Blueprint('account', __name__)
#取得自己的ID
@Account.route('/get_ID', methods=['GET'])
def get_ID():
    if request .method == 'GET':
        if session.get('userType') == userType['USER']:
            if session.get('userID'):
                return jsonify({"rspCode": 200, "ID": session.get('userID')})             #成功取得使用者ID
            else:
                return jsonify({"rspCode": 400})                                #尚未登入
        else:
            return jsonify({"rspCode" : "500"})                                   #權限不符
    else:
        return jsonify({"rspCode": 300})                                    #method使用錯誤

#登出
@Account.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        if session.get('userType') in [userType['AA'], userType['AS'], userType['AU'], userType['AG'], userType['SA']]:
            session.clear()
            return redirect(url_for('Admin.login'))
        elif session.get('userType') == userType['GM']:
            session.clear()
            return redirect(url_for('GM.login'))
        else:
            session.clear()
            return redirect(url_for('USER.index'))


#偵測一般使用者帳號重複(註冊用)
@Account.route('/USER/detect_repeated', methods=['POST'])
def USER_detect_repeated():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        userName = value['userName']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", userName) == None:
            return jsonify({"rspCode": 401})  #帳號格式不符
        else:
            try:
                query_data = account.query.filter(account.userName == func.binary(userName)).first()
            except:
                return jsonify({"rspCode": 400})  #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": 200})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": 402})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": 300})  #methods使用錯誤

#一般使用者註冊
@Account.route('/USER/register', methods=['POST'])
def USER_register():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 412})          #非法字元
        user = []
        user.append(value['name'])
        user.append(value['userName'])
        user.append(value['userPassword'])
        user.append(value['userMail'])
        user.append(value['userPhone'])
        user.append(value['userGender'])
        user.append(value['userBirthday'])
        if len(user[0]) > 20 or len(user[0]) < 1:
            return jsonify({"rspCode": 401})      #名稱長度不符
        elif re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", user[1]) == None:
            return jsonify({"rspCode": 402})      #帳號格式不符
        elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", user[2]) == None:
            return jsonify({"rspCode": 403})      #密碼格式不符
        elif len(user[3]) > 50 or len(user[3]) < 1:
            return jsonify({"rspCode": 404})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", user[3]) == None:
            return jsonify({"rspCode": 405})      #電子郵件格式不符
        elif re.search(r"^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$", user[4]) == None:
            return jsonify({"rspCode": 406})      #手機號碼格式不符
        elif int(user[5]) > 2 or int(user[5]) < 0:
            return jsonify({"rspCode": 407})       #性別異常
        elif re.search(r"^((18|19|20)[0-9]{2})[-\/\.](0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])$", user[6]) == None:
            return jsonify({"rspCode": 408})       #生日格式不符
        else:
            today = datetime.date.today()
            other_day = datetime.date(int(user[6][0:4]), int(user[6][5:7]), int(user[6][8:10]))
            result = other_day - today
            if result.days > 0:
                return jsonify({"rspCode": 409})  #未來人錯誤
            else:
                try:
                    existName = account.query.filter(account.userName == func.binary(user[1])).first()
                    existMail = account.query.filter(account.userMail == func.binary(user[3])).first()
                except:
                    return jsonify({"rspCode": 400})      #資料庫錯誤
                if existName:
                    return jsonify({"rspCode": 410})      #帳號重複
                elif existMail:
                    return jsonify({"rspCode": 411})      #電子郵件重複
                else:
                    try:
                        salt = generate_salt()
                        new_account = account(userName=user[1], name=user[0], userPassword=encrypt(user[2], salt),\
                                            userMail=user[3], userPhone=user[4], userInfo=None, userPoint=0,\
                                            SRRate=None, SRRateTimes=0, SPRate=None, SPRateTimes=0, userGender=user[5],\
                                            userBirthday=user[6], salt=salt)
                        db.session.add(new_account)
                        db.session.commit()
                    except:
                        return jsonify({"rspCode": 400})  #資料庫錯誤
            return jsonify({"rspCode": 200})          #成功註冊
    else:
        return jsonify({"rspCode": 300})  #methods使用錯誤

#一般使用者登入
@Account.route('/USER/login', methods=['POST'])
def USER_login():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        userName = value['userName']
        userPassword = value['userPassword']
        try:
            query_data = account.query.filter(account.userName == func.binary(userName)).first()
        except:
            return jsonify({"rspCode": 400})   #資料庫錯誤
        if query_data == None:    
            return jsonify({"rspCode": 401})   #登入失敗，沒有該帳號
        if check_same(userPassword, query_data.userPassword, query_data.salt):
            session['userID'] = query_data.userID
            session['userType'] = userType['USER']
            return jsonify({"rspCode": 200}) #登入成功
        else:
            return jsonify({"rspCode": 402}) #登入失敗，密碼輸入錯誤       
    else:
        return jsonify({"rspCode": 300})  #methods使用錯誤

#管理員登入
@Account.route('/Admin/login', methods=['POST'])
def Admin_login():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 404})          #非法字元
        adminName = value['adminName']
        adminPassword = value['adminPassword']
        try:
            query_data = adminAccount.query.filter(adminAccount.adminName == func.binary(adminName)).first()
        except:
            return jsonify({"rspCode": 400})                  #資料庫錯誤
        if query_data == None:
            return jsonify({"rspCode": 401})                  #登入失敗，沒有該帳號
        if query_data.adminType not in [userType['SA'], userType['AA'], userType['AS'], userType['AU'], userType['AG']]:
            return jsonify({"rspCode": 402})                  #該帳號非Admin
        if check_same(adminPassword, query_data.adminPassword, query_data.salt) and\
                    query_data.adminType < userType['USER_unverify'] and\
                    query_data.adminType > userType['USER']:
            session['adminID'] = query_data.adminID
            session['userType'] = query_data.adminType
            return jsonify({"rspCode": 200})                  #登入成功
        else:
            return jsonify({"rspCode": 403})                  #登入失敗，密碼錯誤
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤

#GM登入
@Account.route('/GM/login', methods=['POST'])
def GM_login():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 404})          #非法字元
        adminName = value['adminName']
        adminPassword = value['adminPassword']
        try:
            query_data = adminAccount.query.filter(adminAccount.adminName == func.binary(adminName)).first()
        except:
            return jsonify({"rspCode": 400})                  #資料庫錯誤
        if query_data == None:
            return jsonify({"rspCode": 401})                  #登入失敗，沒有該帳號
        if query_data.adminType != userType['GM']:
            return jsonify({"rspCode": 402})                  #該帳號非GM
        if check_same(adminPassword, query_data.adminPassword, query_data.salt) and\
                    query_data.adminType < userType['USER_unverify'] and\
                    query_data.adminType > userType['USER']:
            session['adminID'] = query_data.adminID
            session['userType'] = query_data.adminType
            return jsonify({"rspCode": 200})                  #登入成功
        else:
            return jsonify({"rspCode": 403})                  #登入失敗，密碼錯誤
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤

#一般使用者申請重設密碼信
@Account.route('/USER/forgot_password', methods=['POST'])
def USER_forgot_password():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 405})          #非法字元
        userMail = value['userMail']
        if len(userMail) > 50 or len(userMail) < 1:
            return ({"rspCode": 401})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", userMail) == None:
            return ({"rspCode": 402})      #電子郵件格式不符
        else:
            try:
                query_data = account.query.filter(account.userMail == func.binary(userMail)).first()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            if query_data:
                userID = query_data.userID
                #產生token
                token = USER_forgot_password_token(current_app.config['SECRET_KEY'], userID)
                token_cut = str(token).split("'")[1]
                status = USER_forgot_password_mail(token_cut, userMail)
                if status == {}:
                    return jsonify({"rspCode": 200})     #重置信寄送成功
                else:
                    return jsonify({"rspCode": 404})     #重置信寄送失敗
            else:
                return ({"rspCode": 403})         #電子郵件輸入錯誤，沒有找到對應的電子郵件
    else:
        return ({"rspCode": 300})         #methods使用錯誤

#一般使用者重設密碼
@Account.route('/USER/reset_password', methods=['POST'])
def USER_reset_password():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        token = value['token']
        token_data = validate_token(current_app.config['SECRET_KEY'], token)
        if token_data:
            userPassword = value['userPassword']
            if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,30}$", userPassword) == None:
                return jsonify({"rspCode": 402})      #密碼格式不符
            else:
                try:
                    update_account = account.query.filter(account.userID == func.binary(token_data['userID'])).first()
                    salt = generate_salt()
                    update_account.userPassword = encrypt(userPassword, salt)
                    update_account.salt = salt
                    db.session.commit()
                except:
                    return jsonify({"rspCode": 400})          #資料庫錯誤
                return jsonify({"rspCode": 200})              #重設密碼成功
        else:
            return jsonify({"rspCode": 401})                  #token驗證失敗
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤

#偵測管理員帳號重複(管理員用)
@Account.route('/Admin/detect_repeated', methods=['POST'])
def SA_detect_repeated():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:     
            return jsonify({"rspCode": 409})          #非法字元
        adminName = value['adminName']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", adminName) == None:
            return jsonify({"rspCode": 401})  #帳號格式不符
        else:
            try:
                query_data = adminAccount.query.filter_by(adminName = adminName).first()
            except:
                return jsonify({"rspCode": 400})  #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": 200})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": 402})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": 300})  #methods使用錯誤

#GM註冊
@Account.route('/GM/register', methods=['POST'])
def GM_register():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        GMName = value['GMName']
        GMPassword = value['GMPassword']
        GMMail = value['GMMail']
        GMPhone = value['GMPhone']
        if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", GMName) == None:
            return jsonify({"rspCode": 401})                  #帳號格式不符
        elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", GMPassword) == None:
            return jsonify({"rspCode": 402})                  #密碼格式不符
        elif len(GMMail) > 50 or len(GMMail) < 1:
            return jsonify({"rspCode": 403})                  #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
            return jsonify({"rspCode": 404})                  #電子郵件格式不符
        elif re.search(r"^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$", GMPhone) == None:
            return jsonify({"rspCode": 405})                  #手機號碼格式不符
        else:
            try:
                existName = adminAccount.query.filter(adminAccount.adminName == func.binary(GMName)).first()
                existMail = adminAccount.query.filter(adminAccount.adminMail == func.binary(GMMail)).first()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            if existName:
                if existName != existMail:
                    return jsonify({"rspCode": 406})              #帳號與他人重複
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
                        return jsonify({"rspCode": 400})      #資料庫錯誤
                    token = GM_verify_token(current_app.config['SECRET_KEY'], existMail.adminID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token_cut, GMMail)
                    if status == {}:
                        return jsonify({"rspCode": 200})             #驗證信寄送成功
                    else:
                        return jsonify({"rspCode": 407})             #驗證信寄送失敗
                elif existMail.adminType == userType['GM_apply']:
                    token = GM_verify_token(current_app.config['SECRET_KEY'], existMail.adminID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token_cut, GMMail)
                    if status == {}:
                        return jsonify({"rspCode": 200})             #電子郵件已申請過，驗證信再次寄出
                    else:
                        return jsonify({"rspCode": 407})             #驗證信寄送失敗
                elif existMail.adminType == userType['STOP']:
                    token = GM_verify_token(current_app.config['SECRET_KEY'], existMail.adminID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token_cut, GMMail)
                    if status == {}:
                        return jsonify({"rspCode": 200})             #電子郵件已申請過，驗證信再次寄出
                    else:
                        return jsonify({"rspCode": 407})             #驗證信寄送失敗
                else:
                    return jsonify({"rspCode": 408})          #電子郵件與他人重複
            else:
                try:
                    salt = generate_salt()
                    new_adminAccount = adminAccount(adminName=GMName, adminPassword=encrypt(GMPassword, salt),\
                                                    adminType=userType['GM_apply'], adminPhone=GMPhone, adminMail=GMMail, salt=salt)
                    db.session.add(new_adminAccount)
                    db.session.commit()
                except:
                    return jsonify({"rspCode": 400})          #資料庫錯誤
                token = GM_verify_token(current_app.config['SECRET_KEY'], new_adminAccount.adminID)
                token_cut = str(token).split("'")[1]
                status = GM_verify_mail(token_cut, GMMail)
                if status == {}:
                    return jsonify({"rspCode": 200})             #帳號申請成功，驗證信已寄出
                else:
                    return jsonify({"rspCode": 407})             #驗證信寄送失敗
    else:
        return ({"rspCode": 300})                             #method使用錯誤

#GM驗證結果
@Account.route('/GM/verify/<token>')
def GM_verify(token):
    data = validate_token(current_app.config['SECRET_KEY'], token)
    if data == 'TimeOut':
        return redirect(url_for('GM.verify', result=data))
    if data:
        try:
            query_data = adminAccount.query.filter(adminAccount.adminID == func.binary(data['GMID'])).first()
        except:
            return redirect(url_for('GM.verify', result=1))
        if query_data:
            if query_data.adminType == userType['GM_apply'] or query_data.adminType == userType['STOP']:
                try:
                    query_data.adminType = userType['GM_waiting']
                    db.session.commit()
                except:
                    return redirect(url_for('GM.verify', result=2))
                return redirect(url_for('GM.verify', result=3))
            elif query_data.adminType == userType['GM_unverify']:
                try:
                    query_data.adminType = userType['GM']
                    db.session.commit()
                except:
                    return redirect(url_for('GM.verify', result=4))
                return redirect(url_for('GM.verify', result=5))
            elif query_data.adminType == userType['GM'] or query_data.adminType == userType['GM_waiting']:
                return redirect(url_for('GM.verify', result=6))
        else:
            return redirect(url_for('GM.verify', result=7))
    else:        
        return redirect(url_for('GM.verify', result=8))

'''
#管理員申請重設密碼信
@Account.route('/Admin/forgot_password', methods=['POST'])
def Admin_forgot_password():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        adminMail = value['adminMail']
        print(value)
        if len(adminMail) > 50 or len(adminMail) < 1:
            return jsonify({"rspCode": 401})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", adminMail) == None:
            return jsonify({"rspCode": 402})      #電子郵件格式不符
        else:
            try:
                query_data = adminAccount.query.filter(adminAccount.adminMail == func.binary(adminMail)).first()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            print(query_data)
            if query_data:
                adminID = query_data.adminID
                #產生token
                token = Admin_forgot_password_token(current_app.config['SECRET_KEY'], adminID)
                token_cut = str(token).split("'")[1]
                status = Admin_forgot_password_mail(token_cut, adminMail)
                if status == {}:
                    return jsonify({"rspCode": 200})     #重置信寄送成功
                else:
                    print("寄信失敗\n")
                    return jsonify({"rspCode": 404})     #重置信寄送失敗
            else:
                return jsonify({"rspCode": 403})         #電子郵件輸入錯誤，沒有找到對應的電子郵件
    else:
        return jsonify({"rspCode": 300})         #methods使用錯誤

#管理員重設密碼
@Account.route('/Admin/reset_password/<token>', methods=['POST'])
def Admin_reset_password(token):
    if request.method == 'POST':
        print(token)
        print(request.get_json())
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        print(value)
        token_data = validate_token(current_app.config['SECRET_KEY'], token)
        try:
            adminID = token_data['adminID']
        except:
            return jsonify({"rspCode": 401})                  #token驗證失敗
        adminPassword = value['adminPassword']
        if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,30}$", adminPassword) == None:
            return jsonify({"rspCode": 402})                  #密碼格式不符
        else:                    
            try:
                update_adminAccount = adminAccount.query.filter(adminAccount.adminID == adminID).first()
                salt = generate_salt()
                update_adminAccount.adminPassword = encrypt(adminPassword, salt)
                update_adminAccount.salt = salt
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            return jsonify({"rspCode": 200})                  #重設密碼成功
    else:
        print(300)
        return jsonify({"rspCode": 300})                      #method使用錯誤
'''

#GM申請重設密碼信
@Account.route('/GM/forgot_password', methods=['POST'])
def GM_forgot_password():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 406})          #非法字元
        GMMail = value['GMMail']
        if len(GMMail) > 50 or len(GMMail) < 1:
            return ({"rspCode": 401})      #電子郵件長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
            return ({"rspCode": 402})      #電子郵件格式不符
        else:
            try:
                query_data = adminAccount.query.filter(adminAccount.adminMail == GMMail).first()
            except:
                return jsonify({"rspCode": 400})          #資料庫錯誤
            if query_data:
                if query_data.adminType != userType['GM']:
                    return jsonify({"rspCode": 405})      #該帳號不是GM
                adminID = query_data.adminID
                #產生token
                token = GM_forgot_password_token(current_app.config['SECRET_KEY'], adminID)
                token_cut = str(token).split("'")[1]
                status = GM_forgot_password_mail(token_cut, GMMail)
                if status == {}:
                    return jsonify({"rspCode": 200})     #重置信寄送成功
                else:
                    return jsonify({"rspCode": 404})     #重置信寄送失敗
            else:
                return ({"rspCode": 403})         #電子郵件輸入錯誤，沒有找到對應的電子郵件
    else:
        return ({"rspCode": 300})         #methods使用錯誤

#GM重設密碼
@Account.route('/GM/reset_password', methods=['POST'])
def GM_reset_password():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        token = value['token']
        token_data = validate_token(current_app.config['SECRET_KEY'], token)
        try:
            GMID = token_data['GMID']
        except:
            return jsonify({"rspCode": 401})                  #token驗證失敗
        GMPassword = value['GMPassword']
        if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,30}$", GMPassword) == None:
            return jsonify({"rspCode": 402})                  #密碼格式不符
        else:                    
            try:
                update_adminAccount = adminAccount.query.filter(adminAccount.adminID == GMID).first()
                salt = generate_salt()
                update_adminAccount.adminPassword = encrypt(GMPassword, salt)
                update_adminAccount.salt = salt
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            return jsonify({"rspCode": 200})                  #重設密碼成功
    else:
        return jsonify({"rspCode": 300})                      #method使用錯誤

#設定使用者介紹
@Account.route('/setting/userInfo', methods=['POST'])
def setting_userInfo():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 402})                  #非法字元
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            userInfo = value['userInfo']
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data.userInfo != userInfo:
                    query_data.userInfo = userInfo
                    db.session.commit()
                    return jsonify({"rspCode": 200})          #使用者介紹修改成功
            except:
                return jsonify({"rspCode": 400})              #資料庫錯誤
            return jsonify({"rspCode": 401})                  #介紹並未做更動
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})          #method使用錯誤

#設定名稱
@Account.route('/setting/name', methods=['POST'])
def setting_name():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            name = value['name']
            if len(name) > 20 or len(name) < 1:
                return jsonify({"rspCode": 401})      #名稱長度不符
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data.name != name:
                    query_data.name = name
                    db.session.commit()
                else:
                    return jsonify({"rspCode": 402})  #名稱並未做更動
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #名稱修改成功
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})          #method使用錯誤

#設定使用者名稱
@Account.route('/setting/accountName', methods=['POST'])
def setting_accountName():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 404})          #非法字元
        #驗證身分為一般使用者
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            userName = value['userName']
            if re.search(r"^(?!.*[\u4e00-\u9fa5])\w{1,20}$", userName) == None:
                return jsonify({"rspCode": 401})      #使用者名稱格式不符
            try:
                query_data = account.query.filter(account.userName == func.binary(userName)).first()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            if query_data:
                if query_data.userID == userID:
                    return jsonify({"rspCode": 402})  #使用者名稱並未做更動
                else:
                    return jsonify({"rspCode": 403})      #使用者名稱與他人重複
            try:
                query_data = account.query.filter_by(userID = userID).first()
                query_data.userName = userName
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #一般使用者使用者名稱修改成功
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})              #method使用錯誤

#設定密碼
@Account.route('/setting/accountPassword', methods=['POST'])
def setting_accountPassword():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 404})          #非法字元
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            userPassword = value['userPassword']
            userOldPassword = value['userOldPassword']
            try:
                query_data = account.query.filter_by(userID = userID).first()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            if not check_same(userOldPassword, query_data.userPassword, query_data.salt):
                return jsonify({"rspCode": 401})      #舊密碼錯誤
            if userPassword == userOldPassword:
                return jsonify({"rspCode": 402})      #密碼並未做更動
            if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", userPassword) == None:
                return jsonify({"rspCode": 403})      #密碼格式不符
            try:
                salt = generate_salt()
                query_data.userPassword = encrypt(userPassword, salt)
                query_data.salt = salt
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #密碼修改成功
        elif session.get('userType') in [userType['AA'], userType['AS'], userType['AU'], userType['AG'], userType['GM'], userType['SA']]:
            adminID = session.get('adminID')
            adminPassword = value['adminPassword']
            adminOldPassword = value['adminOldPassword']
            try:
                query_data = adminAccount.query.filter_by(adminID = adminID).first()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            if not check_same(adminOldPassword, query_data.adminPassword, query_data.salt):
                return jsonify({"rspCode": 401})      #舊密碼錯誤
            if adminPassword == adminOldPassword:
                return jsonify({"rspCode": 402})      #密碼並未做更動
            if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", adminPassword) == None:
                return jsonify({"rspCode": 403})      #密碼格式不符
            try:
                salt = generate_salt()
                query_data.adminPassword = encrypt(adminPassword, salt)
                query_data.salt = salt
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #密碼修改成功
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})          #method使用錯誤

#設定電子郵件
@Account.route('/setting/accountMail', methods=['POST'])
def setting_accountMail():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 405})          #非法字元
        if session.get('userType') == userType['USER']:
            userMail = value['userMail']
            userID = session.get('userID')
            if len(userMail) > 50 or len(userMail) < 1:
                return jsonify({"rspCode": 401})      #電子郵件長度不符
            elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", userMail) == None:
                return jsonify({"rspCode": 402})      #電子郵件格式不符
            try:
                existMail = account.query.filter(account.userMail == func.binary(userMail)).first()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            if existMail:
                if existMail.userID == userID:
                    return jsonify({"rspCode": 403})  #電子郵件並未做更動
                else:
                    return jsonify({"rspCode": 404})  #電子郵件已被使用
            try:
                query_data = account.query.filter_by(userID = userID).first()
                query_data.userMail = userMail
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #電子郵件修改成功
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})          #method使用錯誤

#設定手機號碼
@Account.route('/setting/accountPhone', methods=['POST'])
def setting_accountPhone():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        if session.get('userType') == userType['USER']:
            userPhone = value['userPhone']
            userID = session.get('userID')
            if re.search(r"^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$", userPhone) == None:
                return jsonify({"rspCode": 401})      #手機號碼格式不符
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data.userPhone == userPhone:
                    return jsonify({"rspCode": 402})  #手機號碼並未做更動
                query_data.userPhone = userPhone
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #手機號碼修改成功
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})          #method使用錯誤

#設定性別
@Account.route('/setting/userGender', methods=['POST'])
def setting_userGender():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 403})          #非法字元
        if session.get('userType') == userType['USER']:
            userGender = value['userGender']
            userID = session.get('userID')
            if int(userGender) > 2 or int(userGender) < 0:
                return jsonify({"rspCode": 401})      #性別異常
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data.userGender == userGender:
                    return jsonify({"rspCode": 402})  #性別並未做更動
                query_data.userGender = userGender
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #性別修改成功
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})          #method使用錯誤

#設定生日
@Account.route('/setting/userBirthday', methods=['POST'])
def setting_userBirthday():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 404})          #非法字元
        if session.get('userType') == userType['USER']:
            userBirthday = value['userBirthday']
            userID = session.get('userID')
            if re.search(r"^((18|19|20)[0-9]{2})[-\/\.](0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])$", userBirthday) == None:
                return jsonify({"rspCode": 401})       #生日格式不符
            else:
                today = datetime.date.today()
                other_day = datetime.date(int(userBirthday[0:4]), int(userBirthday[5:7]), int(userBirthday[8:10]))
                result = other_day - today
                if result.days > 0:
                    return jsonify({"rspCode": 402})  #未來人錯誤
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if other_day == query_data.userBirthday:
                    return jsonify({"rspCode": 403})  #生日並未做更動
                query_data.userBirthday = userBirthday
                db.session.commit()
            except:
                return jsonify({"rspCode": 400})      #資料庫錯誤
            return jsonify({"rspCode": 200})          #名稱修改成功
        else:
            return jsonify({"rspCode": 500})          #權限不符
    else:
        return jsonify({"rspCode": 300})          #method使用錯誤

#設定個人照片
@Account.route('/setting/propic', methods=['POST'])
def setting_propic():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            f = request.files['propic']
            userID = session.get('userID')
            allowExtention = set(['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'])
            if f and f.filename.rsplit('.', 1)[1] in allowExtention:
                path = current_app.config['UPLOAD_FOLDER'] + "/app/static/img/propic/{}.jpg".format(userID)
                f.save(path)
                return redirect(url_for('USER.setting'))                #成功修改
            else:
                return redirect(url_for('USER.setting'))                #檔名錯誤
        else:
            session.clear()
            return redirect(url_for('USER.index'))                      #權限不符
    else:
        return redirect(url_for('USER.setting'))                        #method使用錯誤

#檢查照片是否存在
@Account.route('/propic_exist', methods=['POST'])
def propic_exist():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": 400, "exist": "0"})            #資料庫錯誤
        userID = value['userID']
        if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + "/app/static/img/propic/"+ str(userID) + ".jpg"):
            return jsonify({"rspCode": 200, "exist": "1"})            #照片存在
        else:
            return jsonify({"rspCode": 200, "exist": "0"})            #照片不存在
    else:
        return jsonify({"rspCode": 300, "exist": "0"})                #method使用錯誤

#取得設定資料
@Account.route('/output/setting_info', methods=['GET'])
def output_setting_info():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data == None:
                    return jsonify({"rspCode": 401})              #ID錯誤
            except:
                return jsonify({"rspCode": 400})                  #資料庫錯誤
            return jsonify({"rspCode": 200, "userID": userID, "userName": query_data.userName, "name": query_data.name,\
                            "userPhone": query_data.userPhone, "userMail": query_data.userMail, "userGender": query_data.userGender,\
                            "userBirthday": str(query_data.userBirthday), "userInfo": query_data.userInfo})             #成功取得個人資料
        else:
            return jsonify({"rspCode": 500})                      #權限不符
    else:
        return jsonify({"rspCode": 300})                          #method使用錯誤