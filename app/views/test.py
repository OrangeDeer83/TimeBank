#coding: utf-8
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, current_app
import re, datetime, smtplib
from sqlalchemy.sql import func
from ..models.model import *
from ..models.dao import *
from ..models.hash import *
from ..models.token import *
from ..models import db
from email.mime.text import MIMEText
test = Blueprint('test', __name__)

@test.route('/USER/detect_repeated', methods=['POST'])
def user_detect_repeated():
    if request.method == 'POST':
        value = request.get_json()
        userID = value['userID']
        if re.search(r"^[\w]{1,20}$", userID) == None:
            return jsonify({"rspCode": "401"})  #帳號格式不符
        else:
            try:
                query_data = account.query.filter(account.userID == func.binary(userID)).first()
            except:
                return jsonify({"rspCode": "400"})  #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": "200"})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": "402"})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

@test.route('/USER/register', methods=['POST'])
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

@test.route('/USER/login', methods=['POST'])
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
            session['userType'] = 1
            return jsonify({"rspCode": "200", "URL": url_for('test.info')}) #登入成功
        else:
            return jsonify({"rspCode": "401", "URL": ""}) #登入失敗       
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤

@test.route('/logout')
def logout():
    if session.get('userID'):
        session.clear()
        return jsonify({"rspCode": "200"})  #登出成功
    else:
        return jsonify({"rspCode": "400"})  #登出失敗

@test.route('/USER/forget_password', methods=['POST'])
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
                token = create_token(current_app.config['SECRET_KEY'], userID, 300)
                token_cut = str(token).split("'")[1]
                #撰寫信件
                mime = MIMEText("點擊以下連結以重設密碼\nhttp://192.168.100.50:5000" +\
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
                status = smtp.sendmail(from_addr, to_addr, msg)
                if status == {}:
                    print("寄信成功\n")
                    smtp.quit()
                    return ({"rspCode": "200"})     #重置信寄送成功
                else:
                    print("寄信失敗\n"  )
                    smtp.quit()
                    return ({"rspCode": "404"})     #重置信寄送失敗
            else:
                return ({"rspCode": "403"})         #信箱輸入錯誤，沒有找到對應的信箱
    else:
        return ({"rspCode": "300"})         #methods使用錯誤

@test.route('/USER/reset_password/<token>', methods=['POST'])
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

@test.route('/create_admins', methods=['POST'])
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
            query_data = adminAccount.query.filter(adminAccount.adminID == func.binary(adminID)).first()
            print(query_data)
        except:
            return jsonify({"rspCode": "400"})          #資料庫錯誤
        if query_data == None:
            try:
                salt = generate_salt()
                print(salt)
                new_adminAccount = adminAccount(adminID=adminID, adminName='admin', adminPassword=encrypt(adminPassword, salt)\
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

@test.route('/delete_admin', methods=['POST'])
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
        return jsonify({"rspCode": "300"})          #method使用錯誤

@test.route('/sql_test')
def sql_test():
    query = task.query.first()
    task.SP.append(userID)
    print(query.SP[0].userName)
    for i in query.SP:
        print(i)

    return 'ok'

@test.route('/login_user_page')
def login_user_page():
    if not (session.get('userID')):
        return render_template('test/navbarVisitor.html')
    else:
        return redirect('/info/' + session.get('userID'))

@test.route('/register_page')
def register_page():
    return render_template('test/register.html')

@test.route('/')
def directory():
    return render_template('test/directory.html')

@test.route('/info')
def info():
    userName =session.get('userName') 
    if not userName:   
        return redirect(url_for('login_user_page'))
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
    return render_template('test/forget_password.html')

@test.route('/USER/reset_password_page/<token>')
def reset_password_page(token):
    print(token)
    if validate_token(current_app.config['SECRET_KEY'], token):
        return render_template('test/reset_password.html')
    else:
        return "該網頁已過期"
