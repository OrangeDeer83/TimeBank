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
import os
import datetime
test = Blueprint('test', __name__)

#設定時間格式
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

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

@test.route('/USER/Register', methods=['POST'])
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


@test.route('/USER/mail', methods=['POST'])
def delete():
    
    return 'ok'

@test.route('/login_user_page')
def login_user_page():
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
       #寫在webIntro.txt(路徑未定)
       file = open(os.getcwd() + '/app/static/uploadFile/' + 'webIntro.txt' , 'w')
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
        #開啟webIntro.txt(路徑未定)
        try:
            file = open(os.getcwd() + '/app/static/uploadFile/' + "webIntro.txt", 'r')
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
        #目前預設傳來的圖片叫做file,允許jpg,gpeg,png(路徑未定)
        allowExtention = set(['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'])
        #檢查fileImage
        if fileImage and '.' in fileImage.filename and fileImage.filename.rsplit('.', 1)[1] in allowExtention:
            try:
                #設定filename = newsID.jpg
                filename = str(db.engine.execute(max_newsID()).fetchone()[0]) + '.jpg'
                #儲存檔案到指定位置(未定)
                fileImage.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage/', filename))
            except:
                #rspCode 402:圖片上傳錯誤
                return jsonify({"rspCode":"402"})
        else:   
            #rspCode 401:圖片檔名錯誤
            return jsonify({"rspCode" : "401"})
        try:    
            #內文上傳
            #(路徑未定)
            fileContentName = str(db.engine.execute(max_newsID()).fetchone()[0]) + '.txt' 
            fileContent = open(os.getcwd() + '/app/static/uploadFile/' +  'newsContent/' + fileContentName, 'w')
            fileContent.write(content)
            fileContent.close()
            return jsonify({"rspCode":"200"})
        except:
            file.close()
            #rspCode 403:內文上傳錯誤
            return jsonify({"rspCode":"403"})
    else:
        return jsonify({"repCode":"300"})

#最新資訊圖片顯示(路徑未定)
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

#最新資訊內文顯示(路徑未定)
#在網址帶入要顯示的編號
#回傳rspCode,content
@test.route("/output_news_content/<number>", methods = ['GET'])
def output_news_content(number):
    if request.method == 'GET':

        try:
            filename = number + '.txt'
            file = open(os.getcwd() + '/app/static/uploadFile/' + 'newsContent/' + filename, 'r')
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
            #允許jpg,gpeg,png(路徑未定)
            allowExtention = set(['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'])
            if fileImage and '.' in fileImage.filename and fileImage.filename.rsplit('.', 1)[1] in allowExtention:
                try:
                    #設定filename = newsID.jpg
                    filename = number + '.jpg'
                    #儲存檔案到指定位置(未定)
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
                if os.path.isfile(os.getcwd() + '/app/static/uploadFile/' + "newsContent/{}.txt".format(number)):
                    file = open(os.getcwd() + '/app/static/uploadFile/' + "newsContent/{}.txt".format(number),'w')
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
        #刪除伺服器中檔案(路徑未定)
        if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage' + "/{}.jpg".format(number)):
            newsImage = current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +'newsImage' + "/{}.jpg".format(number)
        else:
            #rspCode 401:圖片檔案不存在
            return jsonify({"rspCode" : "401"})
        newsContent = os.getcwd() + '/app/static/uploadFile' + "/newsContent/{}.txt".format(number)
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
def userful_numbers():
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

@test.route('/updateWeb')
def updateWeb():
    return render_template('updatewebSA.html')