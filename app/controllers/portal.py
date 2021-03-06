#coding: utf-8
from flask import Blueprint ,url_for, jsonify ,request ,current_app, send_from_directory ,session, redirect
from ..models.model import *
from ..models.dao import *
from ..models import db, userType
import os
import datetime

Portal = Blueprint('portal', __name__)

#入口網站資訊
#網站介紹上傳
#用json傳intro
#回傳rspCode
@Portal.route('/upload_web_intro', methods = ['POST'])
def upload_web_intro():
    if request.method == 'POST':
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AU']):
            return jsonify({"rspCode": 500})
        try:
            adminID = session.get('adminID')
            adminName = db.session.query(adminAccount.adminName).filter(adminAccount.adminID == adminID).first()[0]
            if adminName == None:
                return jsonify({"rspCode": 500})
        except:
            return jsonify({"rspCode": 500})
       #寫在webIntro.txt
        file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'webIntro.txt' , 'w',encoding ='UTF-8')
        try:
            json = request.get_json()
        except:
            return jsonify({"rspCode": 410})
        intro = json['intro']
        if file.write(adminName+"-"):
            if file.write(intro):
                file.close()
                return jsonify({"rspCode": 200})
        else:       
            file.close()       
            #rspCode 400 檔案寫入失敗
            return jsonify({"rspCode" : 400})
    else:
        return jsonify({"rspCode": 300})
 
#網站介紹顯示
#回傳rspCode,webIntro
@Portal.route("/output_webIntro", methods = ['GET'])
def output_web_intro():
    if request.method == 'GET':
        #開啟webIntro.txt
        try:
            file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + "webIntro.txt", 'r',encoding ='UTF-8')
        except:
            #rspCode 400:webIntro.txt開啟失敗
            return jsonify({"rspCode" : 400})
        fileIndex = file.read().split("-")
        webIntro = fileIndex[1]
        adminName = fileIndex[0]
        if session.get('userType') == userType['SA'] or session.get('userType') == userType['AU']:
            intro = jsonify({"rspCode": 200,"webIntro":webIntro,"adminName":adminName})
        else:
            intro = jsonify({"rspCode": 200,"webIntro":webIntro})
        file.close()
        return intro
    else:
        return jsonify({"repCode": 300})    

#最新資訊資訊上傳   
#用form傳title,content,file(jpg,jpeg,png)
@Portal.route('/upload_news', methods = ['POST'])
def upload_news():
    if request.method == 'POST':
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AU']):
            session.clear()
            return "權限不符"
        try:
            adminID = session.get('adminID')
            adminName = db.session.query(adminAccount.adminName).filter(adminAccount.adminID == adminID).first()[0]
            if adminName == None:
                return "權限不符"
        except:
            return "權限不福"
        try:
            title = request.values['title']
            content = request.values['content']
        except:
            return redirect(url_for('Admin.update_web'))
        try:
            fileImage = request.files['file']
        except:
            return redirect(url_for('Admin.update_web'))
        #檢查values是否為空
        if title == '' or content == '' or fileImage.filename == '':
            #rspCode 400:標題,內文,圖片有空值
            return "標題,內文,圖片有空值"
        #檢查tittle有沒有太大
        if len(title) > 30:
            #rspCode 405:title太長
            return "title太長"
        time = str(datetime.datetime.now()).rsplit('.',1)[0]
        try:
            db.engine.execute(insert_news(title,time))
        except:
            #rspCode 404:標題上傳錯誤
            return "標題上傳錯誤"
        #目前預設傳來的圖片叫做file,允許jpg,gpeg,png
        #檢查fileImage
        if fileImage.mimetype == 'image/jpg' or fileImage.mimetype == 'image/png' or fileImage.mimetype == 'image/jpeg':
            try:
                #設定filename = newsID.jpg
                filename = str(db.engine.execute(max_newsID()).fetchone()[0]) + '.jpg'
                #儲存檔案到指定位置
                fileImage.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/newsImage/' , filename))
            except:
                #rspCode 402:圖片上傳錯誤
                return "圖片上傳錯誤"
        else:   
            #rspCode 401:圖片檔名錯誤
            return "圖片檔名錯誤"
        try:    
            #內文上傳
            fileContentName = str(db.engine.execute(max_newsID()).fetchone()[0]) + '.txt' 
            fileContent = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +  'newsContent/' + fileContentName, 'w',encoding ='UTF-8')
            content_ = adminName+"-"+content
            fileContent.write(content_)
            fileContent.close()
            return redirect(url_for('Admin.update_web'))
        except:
            fileContent.close()
            #rspCode 403:內文上傳錯誤
            return "內文上傳錯誤"
    else:
        return "method使用錯誤"

#最新資訊圖片顯示
#在網址帶入要顯示的編號
#回傳rspCode,img
@Portal.route("/output_news_image/<number>", methods = ['GET'])
def output_newsImage(number):
    if request.method == 'GET':
        try:
            if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage' + "/{}.jpg".format(number)):
                filename = number + '.jpg'
                return jsonify({"rspCode": 200, "img": filename})
            else:
                #這個編號沒檔案
                return jsonify({"rspCode":400})
        except:
            #圖片檔名獲取錯誤
            return jsonify({"rspCode" : 400})
    else:
        return jsonify({"rspCode":300})

#最新資訊內文顯示
#在網址帶入要顯示的編號
#回傳rspCode,content
@Portal.route("/output_news_content/<number>", methods = ['GET'])
def output_news_content(number):
    if request.method == 'GET':
        try:
            filename = number + '.txt'
            file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/newsContent/' + filename, 'r', encoding="utf-8")
            file_ = file.read().split("-")
            adminName = file_[0]
            content = ''
            for num in range(len(file_)):
                if num != 0:
                    if num != 1:
                        content += '-'
                    content += file_[num]
            file.close()
            if session.get('userType') == userType['SA'] or session.get('userType') == userType['AU']:
                return jsonify({"rspCode": 200, "content": content,"adminName":adminName})
            else:
                return jsonify({"rspCode": 200, "content": content})
        except:
            #內文顯示錯誤
            return jsonify({"rspCode" : 400})
    else:
        return jsonify({"rspCode":300})
#最新消息標題顯示
#在網址帶入要顯示的編號
#回傳rspCode,title
@Portal.route("/output_news_title/<number>", methods = ['GET'])
def output_news_title(number):
    if request.method == 'GET':
        try:
            return jsonify({"rspCode":200,"title":db.engine.execute(select_title(number)).fetchone()[0]})
        except:
            #最新消息顯示錯誤
            return jsonify({"rspCode": 400})
    else:
        return jsonify({"rspCode":300})
#編輯最新消息
#在網址帶入要編輯的編號
#用form傳file(jpg,png,jpeg),title,content
#回傳rspCode
@Portal.route("/edit_news/<number>", methods = ['POST'])
def edit_news(number):
    if request.method == 'POST':
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AU']):
            session.clear()
            return "權限不符"
        #目前預設傳來的圖片叫做file
        try:
            adminID = session.get('adminID')
            adminName = db.session.query(adminAccount.adminName).filter(adminAccount.adminID == adminID).first()
        except:
            return redirect(url_for('權限不符'))
        try:
            fileImage = request.files['file']
        except:
            return redirect(url_for('圖片檔名錯誤'))
        try:
            title = request.values['title']
            content = request.values['content']
        except:
            return redirect(url_for('輸入錯誤'))
        if len(title) > 30:
            #rspCode 404:title太長
            return "輸入錯誤"
        if fileImage.filename != '':
            #允許jpg,gpeg,png
            if fileImage.mimetype == 'image/jpg' or fileImage.mimetype == 'image/png' or fileImage.mimetype == 'image/jpeg':
                try:
                    #設定filename = newsID.jpg
                    filename = number + '.jpg'
                    #儲存檔案到指定位置
                    os.remove(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage' + "/" + filename)
                    fileImage.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +'newsImage', filename))
                except:
                    #rspCode 401:圖片更新失敗
                    return "圖片更新失敗"
            else:
                #rspCode 400:圖片檔名錯誤
                return "圖片更新失敗"
            
        if title != '':
            try:
               if db.engine.execute(select_title(number)).fetchone() != None:
                    db.engine.execute(update_title(title,number))
               else:
                    return "標題更新失敗"
            except:
                #rspCode 402:標題更新失敗
                return "標題更新失敗"
        if content != '':
            try:
                if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + "newsContent/{}.txt".format(number)):
                    file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + "newsContent/{}.txt".format(number),'w',encoding ='UTF-8')
                    content_ = str(adminName[0])+"-"+str(content)
                    file.write(content_)
                    file.close()
                else:
                    return "內文更新失敗"
            except:
                #rspCode 403:內文更新失敗
                return "內文更新失敗"
        return redirect(url_for('Admin.update_web'))
    else:
        return "伺服器錯誤"
#刪除最新消息
#在網址帶上要刪除的編號 變GET
#回傳rspCode 
@Portal.route("/delete_news/<number>", methods = ['GET'])
def delete_news(number):
    if request.method == 'GET':
        #刪除資料庫中資料
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AU']):
           return jsonify({"rspCode":500})
        try:
            delete_news = news.query.filter_by(newsID = int(number)).first()
            if delete_news != None:
                db.session.delete(delete_news)
                db.session.commit()
            else:
                #rspCode 400:資料庫資料刪除失敗
                return jsonify({"rspCode" : 400})
        except: 
            #rspCode 400:資料庫資料刪除失敗
            return jsonify({"rspCode" : 400})
        #刪除伺服器中檔案
        if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' + 'newsImage' + "/{}.jpg".format(number)):
            newsImage = current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/' +'newsImage' + "/{}.jpg".format(number)
        else:
            #rspCode 401:圖片檔案不存在
            return jsonify({"rspCode" : 401})
        newsContent = current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile' + "/newsContent/{}.txt".format(number)
        try:
            os.remove(newsImage)
        except:
            #rspCode 402:圖片刪除失敗
            return jsonify({"rspCode" : 402})
        try:
            os.remove(newsContent)
            return jsonify({"rspCode" : 200})
        except:
            #rspCode 403:內文刪除失敗
            return jsonify({"rspCode" : 403})
    else:
        return jsonify({"rspCode":300})

#顯示現在有的newsID
#回傳 rspCode 、 number
@Portal.route("/useful_numbers", methods = ['GET'])
def useful_numbers():
    if request.method != "GET":
        return jsonify({"rspCode":300})
    try:
        number_list = []
        number = db.session.query(news.newsID).all()
        for num in number:
            number_list.append(num[0])
        return jsonify({"rspCode":200,"numberList":number_list,"max":number_list[len(number_list)-1]})
    except:
        return jsonify({"rspCode":400})
