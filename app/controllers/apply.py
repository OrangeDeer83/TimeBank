from flask import Blueprint ,url_for, jsonify ,request ,current_app, send_from_directory ,session, redirect
from ..models.model import *
from ..models.dao import *
from ..models import db, userType
import os
import datetime
from ..models.makePoint import *
Apply = Blueprint('apply', __name__)

@Apply.route('/update_apply_group', methods = ['POST'])
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
@Apply.route('/output_apply_group', methods = ['GET'])
def output_apply_group():
    if request.method == "GET":
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA'] or session.get('userType') == userType['USER']):
           return jsonify({"rspCode":"500","allClass":""})
        try:
            file = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile' + '/group_name.txt','r',encoding ='UTF-8')
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
@Apply.route("/output_apply_class" ,methods = ['GET'])
def output_apply_class():
    if request.method == 'GET':
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA'] or session.get('userType') == userType['USER']):
           return jsonify({"rspCode":"500","allClass":""})
        try:
            dbClassData = db.engine.execute(list_alive_apply_className()).fetchall()
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
@Apply.route("/delete_apply_class", methods = ['POST'])
def delete_apply_class():
    if request.method == 'POST':
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA']) :
           return jsonify({"rspCode":"500"})
        try:
            try:
                json = request.get_json()
            except:
                return jsonify({"rspCode":"410"})
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
@Apply.route("/upload_apply_condition_pdf" ,methods = ['POST'])
def upload_apply_condition_pdf():
    if request.method == 'POST':
        #目前預設傳來的東西叫做file,允許pdf
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA']):
            session.clear()
            return redirect(url_for('Admin.update_condition'))
        try:
            filePdf = request.files['file']
        except:
            #檔案傳輸方式錯誤、或是檔案超過2MB
            return redirect(url_for('Admin.update_condition'))
        #檢查fileImage
        if filePdf.mimetype == 'application/pdf':
            try:
                #儲存檔案到指定位置
                filePdf.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile' , '申請說明文件.pdf'))
                return redirect(url_for('Admin.update_condition'))
            except:
                #rspCode 400:圖片上傳錯誤
                return redirect(url_for('Admin.update_condition'))
        else:
            #檔案類型或名稱不許可
            return redirect(url_for('Admin.update_condition'))
    else:
        return redirect(url_for('Admin.update_condition'))
#回傳申請文件名
#回傳rspCode,fileName
@Apply.route("/output_apply_condition_pdf", methods = ['GET'])
def ouput_apply_condition_pdf():
    if request.method == 'GET':
        try:
            if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA'] or session.get('userType') == userType['USER']):
                return jsonify({"rspCode":"500","fileName":""})
            if os.path.isfile(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/'+'申請說明文件.pdf'):
                return jsonify({"rspCode":"200","fileName":"申請說明文件.pdf"})
            else:
                #檔案不存在
                return jsonify({"rspCode":"401","fileName":""})
        except:
            #rspCode 400:回傳失敗
            return jsonify({"rspCode":"400","fileName":""})
    else:
        return jsonify({"repCode":"300","fileName":""})

#新增與更新
#要json傳class,once,one,three,six,year(後面幾個是quota,0為移除)
#回傳rspCode,notAllow
@Apply.route('/update_add_apply_quota' ,methods = ['POST'])
def update_add_apply_quota():
    #try:
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA']):
           return jsonify({"rspCode":"500","notAllow":notAllow})
        if request.method == 'POST':
            try:
                json = request.get_json()
            except:
                return jsonify({"rspCode":"410","notAllow":notAllow}) 
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
            elif len(once) > 2:
                notAllow.append("once")
            if one.isdigit() == False:
                notAllow.append("one")
            elif int(one) < 0:
                notAllow.append("one")
            elif len(one) > 2:
                notAllow.append("one")
            if three.isdigit() == False:
                notAllow.append("three")
            elif int(three) < 0:
                notAllow.append("three")
            elif len(three) > 2:
                notAllow.append("three")
            if six.isdigit() == False:
                notAllow.append("six")
            elif int(six) < 0:
                notAllow.append("six")
            elif len(six) > 2:
                notAllow.append("six")
            if year.isdigit() == False:
                notAllow.append("year")
            elif int(year) < 0:
                notAllow.append("year")
            elif len(year) > 2:
                notAllow.append("year")
            if notAllow != []:
                #rspCode 401:輸入不合法
                return jsonify({"rspCode":"401","notAllow":notAllow})
            
            #一次性
            #檢查是不是0
            if once != '0':
                #檢查原本有沒有這種一次性
                if db.engine.execute(show_quota_by_period_className_alive(className,0)).fetchone() != None:
                    #檢查和已有的once一不一樣，一樣的話不做事
                    if int(once) != db.engine.execute(show_quota_by_period_className_alive(className,0)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_className_period(className,0))
                        db.engine.execute(add_apply_condition(0,className,int(once)))                    
                else:
                    db.engine.execute(add_apply_condition(0,className,int(once)))
            else:
                #檢查有沒有這種一次性
                if db.engine.execute(show_quota_by_period_className_alive(className,0)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_className_period(className,0))
            #一個月
            if one != '0':
                if db.engine.execute(show_quota_by_period_className_alive(className,30)).fetchone() != None:
                    if int(one) != db.engine.execute(show_quota_by_period_className_alive(className,30)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_className_period(className,30))
                        db.engine.execute(add_apply_condition(30,className,int(one)))                    
                else:
                    db.engine.execute(add_apply_condition(30,className,int(one)))
            else:
                if db.engine.execute(show_quota_by_period_className_alive(className,30)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_className_period(className,30))
            #三個月
            if three != '0':
                if db.engine.execute(show_quota_by_period_className_alive(className,90)).fetchone() != None:
                    if int(three) != db.engine.execute(show_quota_by_period_className_alive(className,90)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_className_period(className,90))
                        db.engine.execute(add_apply_condition(90,className,int(three)))                    
                else:
                    db.engine.execute(add_apply_condition(90,className,int(three)))
            else:
                if db.engine.execute(show_quota_by_period_className_alive(className,90)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_className_period(className,90))
            #六個月
            if six != '0':
                if db.engine.execute(show_quota_by_period_className_alive(className,180)).fetchone() != None:
                    if int(six) != db.engine.execute(show_quota_by_period_className_alive(className,180)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_className_period(className,180))
                        db.engine.execute(add_apply_condition(180,className,int(six)))                    
                else:
                    db.engine.execute(add_apply_condition(180,className,int(six)))
            else:
                if db.engine.execute(show_quota_by_period_className_alive(className,180)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_className_period(className,180))
            #一年
            if year != '0':
                if db.engine.execute(show_quota_by_period_className_alive(className,365)).fetchone() != None:
                    if int(year) != db.engine.execute(show_quota_by_period_className_alive(className,365)).fetchone()[0]:
                        db.engine.execute(let_apply_condition_die_className_period(className,365))
                        db.engine.execute(add_apply_condition(365,className,int(year)))                    
                else:
                    db.engine.execute(add_apply_condition(365,className,int(year)))
            else:
                if db.engine.execute(show_quota_by_period_className_alive(className,365)).fetchone() != None:
                     db.engine.execute(let_apply_condition_die_className_period(className,365))
            return jsonify({"rspCode":"200","notAllow":""})
        else:
            return jsonify({"rspCode":"300","notAllow":""})
    #except:
        #rspCode 400:某個地方爆掉但不知道哪裡
        #return jsonify({"rspCode":"400","notAllow":""})

#回傳要求的quota和condition id
#要json傳class,period
#回傳rspCode,conditionID,quota
@Apply.route("/output_quota_conditionID",methods =['POST'])
def output_quota_conditionID():
    if request.method == 'POST':
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA'] or session.get('userType') == userType['USER']):
           return jsonify({"conditionID":"","quota":"","rspCode":"500"})
        try:
            try:
                json = request.get_json() 
            except:
                return jsonify({"conditionID":"","quota":"","rspCode":"410"})
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

#根據所選的class回復period##注意
#要json傳class
#回傳rspCode,periodList
@Apply.route("/output_allow_period", methods = ['POST'])
def return_period_by_class():
    try:
        if request.method == 'POST':
            if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA'] or session.get('userType') == userType['USER']):
                return jsonify({"periodList":"","quotaList":"","rspCode":"500"})
            try:
                json = request.get_json()
            except:
                return jsonify({"periodList":"","quotaList":"","rspCode":"410"}) 
            className = json['class']
            if className == '其他':
                return jsonify({"periodList":"0,30,90,180,365","quotaList":"","rspCode":"200"})
            else:
                dbData = db.engine.execute(out_put_allow_period(className)).fetchall()
                #quotaList = [0,0,0,0,0]
                quotaList = []
                periodList = []
                conditionIDList = []
                
                if dbData != []:
                    for period in dbData:
                        periodList.append(str(period[0]))
                        dbData2 = db.engine.execute(show_quota_conditionID_by_className_period(className,period[0])).fetchone()
                        if period[0] == 0:
                            quotaList.append(str(dbData2[1]))
                        elif period[0] == 30:
                            quotaList.append(str(dbData2[1]))
                        elif period[0] == 90:
                            quotaList.append(str(dbData2[1]))
                        elif period[0] == 180:
                            quotaList.append(str(dbData2[1]))
                        elif period[0] == 365:
                            quotaList.append(str(dbData2[1]))
                    return jsonify({"quotaList":quotaList,"periodList":periodList,"rspCode":"200"})
                else:
                    #rspCode 201:此class沒有可被申請的週期
                    return jsonify({"quotaList":"","periodList":"","rspCode":"201"})
        else:
            return jsonify({"quotaList":"","periodList":"","rspCode":"300"})
    except:
            #rspCode 400:某個地方爆掉
            return jsonify({"periodList":"","quotaList":"","rspCode":"400"})

#使用者新增申請
#要form傳frequency,period,result,class,quota,file(pdf)
#回傳rspCode,notAllow
@Apply.route("/USER/add_apply", methods = ['POST'])
def user_add_apply():
    #try:
        if request.method == 'POST':
            if not(session.get('userType') == userType['USER']):
                session.clear()
                return redirect(url_for('USER.application'))
            notAllow = []
            try:
                userID = session.get('userID')
            except:
                session.clear()
                return redirect(url_for('USER.application'))
            time = str(datetime.datetime.now()).rsplit('.',1)[0]
            #檢查各變數與檔案
            if request.values['applyFrequency'].isdigit():
                if int(request.values['applyFrequency']) > 0 and len(request.values['applyFrequency']) < 6:
                    frequency = int(request.values['applyFrequency'])
                else:
                    frequency = 0
                    notAllow.append('applyFrequency')
            else:
                frequency = 0
                notAllow.append('applyFrequency')
            if request.values['applyPeriod'] in ['0','30','90','180','365']:
                restTime = int(request.values['applyPeriod']) * frequency
                nextTime = int(request.values['applyPeriod'])
            else:
                notAllow.append('applyPeriod')
            result = request.values['applyReason']        
            if(request.values['class'] != '其他'):
                try:
                    if notAllow != []:
                        #rspCode 403:有輸入不符合格式
                        return jsonify({"notAllow":notAllow,"rdpCode":"403"})
                        #return redirect(url_for('USER.application'))
                    conditionID = db.engine.execute(show_conditionID(request.values['class'],request.values['applyPeriod'])).fetchone()[0]
                except:
                    #rspCode 401:找不到conditionID
                    #return jsonify({"rspCode":"401","notALlow":""})
                    return redirect(url_for('USER.application'))
            else:
                if result == '':
                    #rspCode 402:其他要填原因
                    #return jsonify({"rspCode":"402","notALlow":""})
                    return redirect(url_for('USER.application'))
                #檢查其他的quota
                if request.values['applyQuota'].isdigit():
                    if int(request.values['applyQuota']) > 0 and len(request.values['applyQuota']) < 6:
                        quota = request.values['applyQuota']
                    else:
                        notAllow.append('applyQuota')
                else:
                    notAllow.append('applyQuota')
                if notAllow != []:
                    #rspCode 403:有輸入不符合格式
                    #return jsonify({"notAllow":notAllow,"rdpCode":"403"})
                    return redirect(url_for('USER.application'))
                #檢查有沒有一樣的其他了
                if db.engine.execute(find_other_apply_condition_id(nextTime,quota)).fetchone() != None:
                    conditionID = db.engine.execute(find_other_apply_condition_id(nextTime,quota)).fetchone()[0]
                #沒有才建新的
                else:
                    db.engine.execute(set_up_apply_condition('其他',nextTime,quota))
                    conditionID = db.engine.execute(find_other_apply_condition_id(nextTime,quota)).fetchone()[0]
 
            try:
                file = request.files['applyDocument']
            except:
                apply_condition = db.session.query(applyCondition).filter(applyCondition.conditionID == conditionID).first()
                db.session.delete(apply_condition)
                db.session.commit()
                
                return redirect(url_for('USER.application'))
            #建立apply
            db.engine.execute(add_apply(frequency,restTime,nextTime,userID,conditionID,result,time))   
            #檢查有沒有傳檔案
            if file.filename != "":
                try:
                    print(file.filename)
                    #檢查fileName
                    if file.mimetype == 'application/pdf':
                        originFileName = '{}'.format(file.filename)
                        num = str(db.engine.execute(find_max_applyId_by_user_ID(userID)).fetchone()[0])
                        os.makedirs(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}'.format(num))
                        fileTxt =open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}/{}.txt'.format(num,num), 'w', encoding="utf-8")
                        fileTxt.write(file.filename)
                        fileTxt.close()
                        #儲存檔案到指定位置
                        filename = '{}.pdf'.format(num)
                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}'.format(num),filename))
                except:
                    #rspCode 404:pdf上傳錯誤
                    #return jsonify({"rspCode":"404","notALlow":""})
                    return redirect(url_for('USER.application'))
            #return jsonify({"rspCode":"200","notALlow":""})
            return redirect(url_for('USER.application'))
        else:
            #return jsonify({"rspCode":"300","notALlow":""})
            return redirect(url_for('USER.application'))
    #except:
        #rspCode 400:某個地方爆掉但不知道哪裡
        #return jsonify({"rspCode":"400","notALlow":""})
        return redirect(url_for('USER.application'))


#審核申請資料顯示
#要json傳(userName,name)(搜尋目標，沒有就傳空值)
#回傳rspCode, userName, userSRRate, userSPRate, applyPdfName, applyID,
#applyClass, applyQuota, applyPeriod, applyFrequency, applyTime, applyResult,
#userID
@Apply.route('/show_apply_status_0', methods = ['POST'])
def show_apply_status_0():
    if request.method == 'POST':
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA']):
            return jsonify({"rspCode":"500","name":"","userSRRate":"","userSPRate":"","applyPdfName":"","applyID":"","applyClass":"","applyQuota":"","applyPeriod":"","applyFrequency":"","applyTime":"","applyResult":"","userID":""})
        try:
            json = request.get_json()
        except:
            return jsonify({"rspCode":"410","name":"","userSRRate":"","userSPRate":"","applyPdfName":"","applyID":"","applyClass":"","applyQuota":"","applyPeriod":"","applyFrequency":"","applyTime":"","applyResult":"","userID":""})
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
            return jsonify({"rspCode":"401","name":"","userSRRate":"","userSPRate":"","applyPdfName":"","applyID":"","applyClass":"","applyQuota":"","applyPeriod":"","applyFrequency":"","applyTime":"","applyResult":"","userID":""})
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
               applyTime.append(str(oneData[3]))
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
@Apply.route('/simple_personal_apply_history',methods =['POST'])
def simple_personal_apply_history():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","applyTime":"","frequency":"","result":"","status":"","judgeTime":"","period":"","className":"","quota":"","oldQuota":"","applyPdfName":"","applyID":"","userID":"","name":""})
    if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA']):
        return jsonify({"rspCode":"500","applyTime":"","frequency":"","result":"","status":"","judgeTime":"","period":"","className":"","quota":"","oldQuota":"","applyPdfName":"","applyID":"","userID":"","name":""})
    try:
        json = request.get_json()
    except:
        return jsonify({"rspCode":"410","applyTime":"","frequency":"","result":"","status":"","judgeTime":"","period":"","className":"","quota":"","oldQuota":"","applyPdfName":"","applyID":"","userID":"","name":""})
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
        applyTime.append(str(apply[1]))
        frequency.append(apply[2])
        result.append(apply[3])
        status.append(apply[4])
        judgeTime.append(str(apply[6]))
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
@Apply.route('/apply_pdf_download/<number>', methods = ['GET'])
def apply_pdf_download(number):
    if request.method != 'GET':
        return jsonify({"rspCode":"300"})
    if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA'] or session.get('userType') == userType['USER']):
        return jsonify({"rspCode":"500"})
    try:
        applyID = number
        filename = open(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}/{}.txt'.format(applyID, applyID), 'r', encoding='utf-8').read()
        print(filename)
        return send_from_directory(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/apply_pdf/{}'.format(applyID),filename,as_attachment=True)
    except:
        #rspCode 400:檔案不存在
        return jsonify({"rspCode":"400"})

#決定申請是否通過###
#要json傳 applyID,applyStatus(案的是核准就給1沒過給2),quotaChange(核准額度有變給值，沒有傳空)
#回傳 rspCode,notAllow
@Apply.route('/apply_judge', methods = ['POST'])
def apply_judge():
    if request.method != 'POST':
        return jsonify({"rspCode":"300"})
    if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA']):
        return jsonify({"rspCode":"500","notAllow":""}) 
    try:
        json = request.get_json()
    except:
        return jsonify({"rspCode":"410","notAllow":""})
    try:
        adminID = session.get('adminID')
    except:
        return jsonify({"rspCode":"500","notAllow":""}) 
    applyID = json['applyID']
    applyStatus = json['applyStatus']
    quotaChange = json['quotaChange']
    notAllow = []
    
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
        if applyStatus == '1':
            
            userID = db.engine.execute(get_userID_by_applyID(applyID)).fetchone()[0]
            userPoint = db.engine.execute(get_user_point(userID)).fetchone()[0]
            ConditionID = db.engine.execute(get_conditionID(applyID)).fetchone()[0]
            conditionData = db.engine.execute(show_old_condition_data(ConditionID)).fetchone()
            quota = conditionData[2]
            period = conditionData[0]
            plus = userPoint + int(quota)
            if period != 0:
                rest = db.engine.execute(show_rest_time_by_applyID(applyID)).fetchone()[0]
                db.engine.execute(alter_apply_rest_time(applyID,rest - period))
            u = db.session.query(account).filter(account.userID == userID).first()
            u.userPoint = plus
            db.session.commit()
            for x in range(int(quota)):
                pointID = make_point()+"_{}".format(str(db.session.query(point).count() + 1))
                db.engine.execute(make_point_sql(pointID,adminID,userID))
                db.session.commit()     
            transferRecord_ = transferRecord(userID = userID,time = datetime.datetime.now())
            db.session.add(transferRecord_)
            db.session.commit()
            transferRecordApply_ = transferRecordApply(transferRecordID = transferRecord_.transferRecordID, applyID = applyID, times = 1)
            db.session.add(transferRecordApply_)
            db.session.commit()
            transferRecord_ = transferRecord(userID = userID,time = datetime.datetime.now())
            db.session.add(transferRecord_)
            db.session.commit()
            transferRecordApply_ = transferRecordApply(transferRecordID = transferRecord_.transferRecordID, applyID = applyID, times = 1)
            db.session.add(transferRecordApply_)
            db.session.commit()
        else:
            #不是1就只改status和adminID
            db.engine.execute(alter_apply_status(applyStatus,applyID))
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
                db.engine.execute(set_up_special_apply_condition(className,period,quotaChange))
                newConditionID = db.session.query(applyCondition.conditionID).filter(applyCondition.className == className).filter(applyCondition.period == period).filter(applyCondition.quota == quotaChange).first()[0]
                
            else:
                newConditionID = db.engine.execute(find_special_apply_condition(className,period,quotaChange)).fetchone()[0]
            db.engine.execute(alter_oldConditionID(oldConditionID,applyID))
            db.engine.execute(alter_conditionID_in_apply(newConditionID,applyID))
            db.engine.execute(alter_apply_status(applyStatus,applyID))
            userID = db.engine.execute(get_userID_by_applyID(applyID)).fetchone()[0]
            userPoint = db.engine.execute(get_user_point(userID)).fetchone()[0]
            plus = userPoint + int(quotaChange)
            db.engine.execute(plus_user_point(plus,userID))
            if period != 0:
                rest = db.engine.execute(show_rest_time_by_applyID(applyID)).fetchone()[0]
                db.engine.execute(alter_apply_rest_time(applyID,rest - period))
            for x in range(int(quotaChange)):
                pointID = make_point()+"_{}".format(str(db.session.query(point).count() + 1))
                db.engine.execute(make_point_sql(pointID,adminID,userID))
                db.session.commit()
            transferRecord_ = transferRecord(userID = userID,time = datetime.datetime.now())
            db.session.add(transferRecord_)
            db.session.commit()
            transferRecordApply_ = transferRecordApply(transferRecordID = transferRecord_.transferRecordID, applyID = applyID, times = 1)
            db.session.add(transferRecordApply_)
            db.session.commit()
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
@Apply.route('/judgement_history', methods = ['POST'])
def judgement_history():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","userID":"","userSRRate":"","userSPRate":"","name":"","applyPdfName":"","applyID":"","className":"","quota":"","oldQuota":"","applyTime":"","judgeTime":"","period":"","applyResult":"","applyStatus":"","applyFrequency":""})
    try:
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AA']):
            return jsonify({"rspCode":"500","userID":"","userSRRate":"","userSPRate":"","name":"","applyPdfName":"","applyID":"","className":"","quota":"","oldQuota":"","applyTime":"","judgeTime":"","period":"","applyResult":"","applyStatus":"","applyFrequency":""})
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
        try:
            json = request.get_json()
        except:
            return jsonify({"rspCode":"410","userID":"","userSRRate":"","userSPRate":"","name":"","applyPdfName":"","applyID":"","className":"","quota":"","oldQuota":"","applyTime":"","judgeTime":"","period":"","applyResult":"","applyStatus":"","applyFrequency":""})
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

            userName.append(userData[0])
        return jsonify({"rspCode":"200","userID":userID,"userSRRate":userSRRate,"userSPRate":userSPRate,"name":userName,"applyPdfName":applyPdfName,"applyID":applyID,"className":applyClass,"quota":applyQuota,"oldQuota":oldQuota,"applyTime":applyTime,"judgeTime":judgeTime,"period":applyPeriod,"applyResult":result,"applyStatus":applyStatus,"applyFrequency":frequency})
    except:
        return jsonify({"rspCode":"400","userID":"","userSRRate":"","userSPRate":"","name":"","applyPdfName":"","applyID":"","className":"","quota":"","oldQuota":"","applyTime":"","judgeTime":"","period":"","applyResult":"","applyStatus":"","applyFrequency":""})

#下載申請說明文件
@Apply.route("/download/申請說明文件",methods = ['GET'])
def download_apply_description():
    if request.method != 'GET':
        return jsonify({"rspCode":"300"})
    if session.get('userType') != userType['SA'] or session.get('userType') != userType['AA']  or session.get('userType') != userType['USER']:
        return jsonify({"rspCode":"500"})
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'] + '/app/static/uploadFile/','申請說明文件.pdf',as_attachment=True)
    except:
        return jsonify({"rspCode":"400"})

