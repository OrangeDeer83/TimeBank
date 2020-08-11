#coding: utf-8
from flask import Blueprint, render_template, session, url_for, jsonify, request, current_app
import re, datetime, smtplib, random
from sqlalchemy.sql import func
from ..models.hash import *
from ..models.token import *
from ..models.model import *
from ..models.mail import *
from ..models import db
from email.mime.text import MIMEText

Account = Blueprint('account', __name__)

'''
GM狀態:     SA填寫Email | GM註冊 | GM點擊驗證連結 |  名稱
                1           0           0         unverify
                0           1           0           apply
                0           1           1         waitting
'''
userType = {'USER': 1, 'AS': 2, 'AA': 3, 'AU': 4, 'AG': 5, 'GM': 6, 'SA': 7,
            'USER_unverify': 8, 'AS_unverify': 9, 'AA_unverify': 10,
            'AU_unverify': 11, 'AG_unverify': 12, 'GM_unverify': 13,
            'SA_unverify': 14, 'GM_apply': 15, 'GM_waitting': 16}

#偵測一般使用者帳號重複(註冊用)
@Account.route('/USER/detect_repeated', methods=['POST'])
def user_detect_repeated():
    if request.method == 'POST':
        value = request.get_json()
        userID = value['userID']
        if re.search(r"^\w{1,20}$", userID) == None:
            return jsonify({"rspCode": "401"})  #帳號格式不符
        else:
            #try:
            query_data = account.query.filter(account.userID == func.binary(userID)).first()
            #except:
            #    return jsonify({"rspCode": "400"})  #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": "200"})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": "402"})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤


#一般使用者註冊
@Account.route('/USER/register', methods=['POST'])
def user_register():
    if request.method == 'POST':
        value = request.get_json()
        user = []
        user.append(value['userName'])
        user.append(value['userID'])
        user.append(value['userPassword'])
        user.append(value['userMail'])
        user.append(value['userPhone'])
        user.append(value['userGender'])
        user.append(value['userBirthday'])
        if len(user[0]) > 20 or len(user[0]) < 1:
            return jsonify({"rspCode": "401"})      #名稱長度不符
        elif re.search(r"^\w{1,20}$", user[1]) == None:
            return jsonify({"rspCode": "402"})      #帳號格式不符
        elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", user[2]) == None:
            return jsonify({"rspCode": "403"})      #密碼格式不符
        elif len(user[3]) > 50 or len(user[3]) < 1:
            return jsonify({"rspCode": "404"})      #信箱長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", user[3]) == None:
            return jsonify({"rspCode": "405"})      #信箱格式不符
        elif re.search(r"\d{1,20}", user[4]) == None:
            return jsonify({"rspCode": "406"})      #電話格式不符
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
                    existID = account.query.filter(account.userID == func.binary(user[1])).first()
                    existMail = account.query.filter(account.userMail == func.binary(user[3])).first()
                except:
                    return jsonify({"rspCode": "400"})      #資料庫錯誤
                if existID:
                    return jsonify({"rspCode": "410"})      #帳號重複
                elif existMail:
                    return jsonify({"rspCode": "411"})      #信箱重複
                else:
                    try:
                        salt = generate_salt()
                        new_account = account(userID=user[1], userName=user[0], userPassword=encrypt(user[2], salt),\
                                            userMail=user[3], userPhone=user[4], userInfo=None, userPoint=0,\
                                            SRRate=None, SRRateTimes=0, SPRate=None, SPRateTimes=0, userGender=user[5],\
                                            userBirthday=user[6], salt=salt)
                        db.session.add(new_account)
                        db.session.commit()
                    except:
                        return jsonify({"rspCode": "400"})  #資料庫錯誤
            return jsonify({"rspCode": "200"})          #成功註冊
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

#一般使用者登入
@Account.route('/USER/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        value = request.get_json()
        print(value) 
        userID = value['userID']
        userPassword = value['userPassword']
        try:
            query_data = account.query.filter(account.userID == func.binary(userID)).first()
            print(query_data)
        except:
            return jsonify({"rspCode": "400", "URL": ""})   #資料庫錯誤
        if check_same(userPassword, query_data.userPassword, query_data.salt):
            session['userID'] = userID
            session['userName'] = query_data.userName
            session['userType'] = userType['USER']
            return jsonify({"rspCode": "200", "URL": url_for('test.info')}) #登入成功
        else:
            return jsonify({"rspCode": "401", "URL": ""}) #登入失敗       
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

#登出
@Account.route('/logout')
def logout():
    if session.get('userID'):
        session.clear()
        return jsonify({"rspCode": "200"})  #登出成功
    else:
        return jsonify({"rspCode": "400"})  #登出失敗

#申請重設密碼信
@Account.route('/USER/forget_password', methods=['POST'])
def user_forget_password():
    if request.method == 'POST':
        value = request.get_json()
        userMail = value['userMail']
        print(value)
        if len(userMail) > 50 or len(userMail) < 1:
            return ({"rspCode": "401"})      #信箱長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", userMail) == None:
            return ({"rspCode": "402"})      #信箱格式不符
        else:
            try:
                query_data = account.query.filter(account.userMail == func.binary(userMail)).first()
            except:
                return jsonify({"rspCode": "400"})      #資料庫錯誤
            print(query_data)
            if query_data:
                userID = query_data.userID
                #產生token
                token = user_forget_password_token(current_app.config['SECRET_KEY'], userID)
                token_cut = str(token).split("'")[1]
                status = forget_password_mail(token_cut, userMail)
                if status == {}:
                    print("寄信成功\n")
                    return ({"rspCode": "200"})     #重置信寄送成功
                else:
                    print("寄信失敗\n"  )
                    return ({"rspCode": "404"})     #重置信寄送失敗
            else:
                return ({"rspCode": "403"})         #信箱輸入錯誤，沒有找到對應的信箱
    else:
        return ({"rspCode": "300"})         #methods使用錯誤

#重設密碼
@Account.route('/USER/reset_password/<token>', methods=['POST'])
def user_reset_password(token):
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

#偵測管理員帳號重複(SA新增管理員用)
@Account.route('/SA/detect_repeated', methods=['POST'])
def SA_detect_repeated():
    if request.method == 'POST':
        value = request.get_json()
        adminID = value['adminID']
        print(value)
        if re.search(r"^\w{1,20}$", adminID) == None:
            return jsonify({"rspCode": "401"})  #帳號格式不符
        else:
            try:
                query_data = adminAccount.query.filter_by(adminID = adminID).first()
            except:
                return jsonify({"rspCode": "400"})  #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": "200"})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": "402"})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

#新增管理員
@Account.route('/create_admins', methods=['POST'])
def create_admins():
    if request.method == 'POST':
        value = request.get_json()
        print(value)
        adminType = value['adminType']
        if int(adminType) > 5 or int(adminType) < 2:
            return jsonify({"rspCode": "401"})          #管理員權限不符
        adminID = value['adminID']
        if re.search(r"^\w{1,20}$", adminID) == None:
            return jsonify({"rspCode": "402"})          #帳號格式不符
        adminPassword = value['adminPassword']
        if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", adminPassword) == None:
            return jsonify({"rspCode": "403"})          #密碼格式不符
        try:
            query_data = adminAccount.query.filter_by(adminID = adminID).first()
            print(query_data)
        except:
            return jsonify({"rspCode": "400"})          #資料庫錯誤
        if query_data == None:
            try:
                salt = generate_salt()
                print(salt)
                new_adminAccount = adminAccount(adminID=adminID, adminName='admin', adminPassword=encrypt(adminPassword, salt)\
                                                , adminType=adminType + 7, adminPhone=None,adminMail=None, salt=salt)
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
@Account.route('/delete_admin', methods=['POST'])
def delete_admin():
    if request.method == 'POST':
        value = request.get_json()
        adminID = value['adminID']
        try:
            SA_data = adminAccount.query.filter(adminAccount.adminType == 7).first()
        except:
            return jsonify({"rspCode": "400"})              #資料庫錯誤
        if session.get('SALogin') == SA_data.adminPassword:
            try:
                query_data = adminAccount.query.filter(adminAccount.adminID == func.binary(adminID)).first()
                if query_data == None:
                    return jsonify({"rspCode": "401"})  #adminID不在資料庫中，前端可能遭到竄改
                db.session.delete(query_data)
                db.session.commit()
            except:
                return jsonify({"rspCode": "400"})          #資料庫錯誤
            return jsonify({"rspCode": "200"})              #刪除成功
        else:
            SAPassword = value['SAPassword']
            if SAPassword == None:
                return ({"rspCode": "401"})                 #尚未輸入第一次密碼
            if check_same(SAPassword, SA_data.adminPassword, SA_data.salt):
                session['SALogin'] = SA_data.adminPassword
                try:
                    query_data = adminAccount.query.filter(adminAccount.adminID == func.binary(adminID)).first()
                    if query_data == None:
                        return jsonify({"rspCode": "402"})  #adminID不在資料庫中，前端可能遭到竄改
                    db.session.delete(query_data)
                    db.session.commit()
                except:
                    return jsonify({"rspCode": "400"})      #資料庫錯誤
            else:
                return jsonify({"rspCode": "403"})          #密碼輸入錯誤
        return jsonify({"rspCode": "200"})                  #刪除成功
    else:
        return jsonify({"rspCode": "300"})                  #method使用錯誤

#輸入GM申請email
@Account.route('/load_GM_mail', methods=['POST'])
def load_GM_mail():
    if request.method == 'POST':
        value = request.get_json()
        GMMail = value['GMMail']
        if re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
            return ({"rspCode": "401"})                     #信箱格式不符
        try:
            adminID = generate_salt()
            query_data = adminAccount.query.filter_by(adminID = adminID).first()
            while query_data:
                adminID = generate_salt()
                query_data = adminAccount.query.filter_by(adminID = adminID).first()
            new_adminAccount = adminAccount(adminID=userID, adminName='admin', adminPassword='None'\
                                            , adminType=userType['GM_unverify'], adminPhone=None,\
                                            adminMail=None, salt='None')
            db.session.add(new_adminAccount)
            db.session.commit()
        except:
            return jsonify({"rspCode": "400"})              #資料庫錯誤
        return jsonify({"rspCode": "200"})                  #email輸入成功
    else:
        return jsonify({"rspCode": "300"})                  #method使用錯誤
    
#GM註冊
@Account.route('/GM/register', methods=['POST'])
def GM_register():
    if request.method == 'POST':
        value = request.get_json()
        GMID = value['GMID']
        GMPassword = value['GMPassword']
        GMMail = value['GMMail']
        GMPhone = value['GMPhone']
        if re.search(r"^\w{1,20}$", GMID) == None:
            return jsonify({"rspCode": "401"})                  #帳號格式不符
        elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", GMPassword) == None:
            return jsonify({"rspCode": "402"})                  #密碼格式不符
        elif len(GMMail) > 50 or len(GMMail) < 1:
            return jsonify({"rspCode": "403"})                  #信箱長度不符
        elif re.search(r"^[\w\-\.]+\@[\w\-\.]+\.[0-9a-zA-Z]+$", GMMail) == None:
            return jsonify({"rspCode": "404"})                  #信箱格式不符
        elif re.search(r"\d{1,20}", GMPhone) == None:
            return jsonify({"rspCode": "405"})                  #電話格式不符
        else:
            try:
                existID = adminAccount.query.filter(adminAccount.adminID == func.binary(GMID)).first()
                existMail = adminAccount.query.filter(adminAccount.adminMail == func.binary(GMMail)).first()
            except:
                return jsonify({"rspCode": "400"})              #資料庫錯誤
            if existID:
                return jsonify({"rspCode": "407"})              #帳號重複
            if existMail:
                if existMail.adminType == userType['GM_unverify']:
                    try:
                        salt = generate_salt()
                        existMail.adminName = adminName
                        existMail.adminPassword = encrypt(adminPassword, salt)
                        existMail.adminPhone = adminPhone
                        existMail.salt = salt
                        db.session.commit()
                    except:
                        return jsonify({"rspCode": "400"})      #資料庫錯誤
                    token = GM_verify_token(current_app.config['SECRET_KEY'], GMID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token, GMMail)
                    if status == {}:
                        print("寄信成功\n")
                        return ({"rspCode": "200"})             #驗證信寄送成功
                    else:
                        print("寄信失敗\n"  )
                        return ({"rspCode": "404"})             #驗證信寄送失敗
                elif existMail.adminType == userType['GM_apply']:
                    token = GM_verify_token(current_app.config['SECRET_KEY'], GMID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token, GMMail)
                    if status == {}:
                        print("寄信成功\n")
                        return ({"rspCode": "201"})             #信箱已申請過，驗證信再次寄出
                    else:
                        print("寄信失敗\n"  )
                        return ({"rspCode": "405"})             #驗證信寄送失敗
                else:
                    return jsonify({"rspCode": "406"})          #信箱重複
            else:
                try:
                    salt = generate_salt()
                    new_adminAccount = adminAccount(adminName=GMName, adminPassword=encrypt(GMPassword, salt),\
                                                    adminType=userType['GM_apply'], adminPhone=GMPhone, adminMail=GMMail, salt=salt)
                    db.session.add(new_adminAccount)
                    db.session.commit()
                except:
                    return jsonify({"rspCode": "400"})          #資料庫錯誤
                    token = GM_verify_token(current_app.config['SECRET_KEY'], GMID)
                    token_cut = str(token).split("'")[1]
                    status = GM_verify_mail(token, GMMail)
                    if status == {}:
                        print("寄信成功\n")
                        return ({"rspCode": "202"})             #帳號申請成功，驗證信已寄出
                    else:
                        print("寄信失敗\n"  )
                        return ({"rspCode": "407"})             #驗證信寄送失敗
    else:
        return ({"rspCode": "300"})                             #method使用錯誤



@Account.route('/GM/verify/<token>', methods=['POST'])
def GM_verify(token):
    