#coding: utf-8
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
import re, datetime
from sqlalchemy.sql import func
from ..models.model import *
from ..models.dao import *
from ..models.hash import *
from ..models import db
test = Blueprint('test', __name__)

@test.route('/USER/detect_repeated', methods=['POST'])
def user_detect_repeated():
    if request.method == 'POST':
        value = request.get_json()
        userID = value['userID']
        print(userID)
        if re.search(r"^[\w]{1,20}$", userID) == None:
            return jsonify({"rspCode": "401"})  #帳號格式不符
        else:
            try:
                query_data = account.query.filter(account.userID == func.binary(userID)).first()
            except:
                return jsonify({"rspCode": "402"})  #資料庫錯誤
            if query_data == None:
                print(200)
                return jsonify({"rspCode": "200"})  #沒有重複帳號，帳號可使用
            else:
                return jsonify({"rspCode": "400"})  #偵測到重複帳號，帳號無法使用
    else:
        return jsonify({"rspCode": "300"})  #methods使用錯誤



@test.route('/USER/register', methods=['POST'])
def user_register():
    if request.method == 'POST':
        value = request.get_json()
        print(value)
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



@test.route('/USER/mail', methods=['POST'])
def delete():
    json = request.get_json()
    if re.search(r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$", json['userMail']) == None:
        return jsonify({"rspCode": "405"})      #信箱格式不符
    else:
        return 'good'
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

@test.route('/info/<userID>')
def info(userID):
    if not session.get('userID'):   
        return redirect(url_for('login_user_page'))
    else:
        return render_template('test/directory.html', welcome = '歡迎' + userID)

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


'''
@test.route('/reset_password_page/<token>')
def reset_password_page(token):
    print(token)
    if validate_token(token):
        return render_template('test/reset_password.html')
    else:
        return "該網頁已過期"
'''