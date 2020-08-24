from flask import Blueprint , jsonify ,request, send_from_directory ,session
from ..models.model import *
from ..models.dao import *
from ..models import db, userType
from ..models.makePoint import *
import datetime
Allotment = Blueprint('allotment', __name__)


#顯示user名單
#要json傳target(搜尋目標，沒有就傳空值)
#回傳rspCode, userName, userID, userSRRate, userSPRate
@Allotment.route('/show_user', methods = ['POST'])
def show_user():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","name":"","userID":"","userSRRate":"","userSPRate":""})
    try:
        json = request.get_json()
    except:
        return jsonify({"rspCode":"410","name":"","userID":"","userSRRate":"","userSPRate":""})
    if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AS']):
        return jsonify({"rspCode":"500","name":"","userID":"","userSRRate":"","userSPRate":""})
    #搜尋的東西
    target = json['target']
    userID = []
    userSRRate = []
    userSPRate = []
    userName = [] 
    userPoint= []
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
        userPoint.append(user[6])
    return jsonify({"rspCode":"200","userID":userID,"name":userName,"userSRRate":userSRRate,"userSPRate":userSPRate,"userPoint":userPoint})

#配發按鍵
#要json傳kind(one or all), receiver(one時是目標的ID all是搜尋了什麼), period,
#frequency(一次性傳1), quota
#回傳rspCode 和 notAllow
@Allotment.route("/allotment" , methods = ['POST'])
def allotment():
    try:
        json = request.get_json()
    except:
        return jsonify({"rspCode":"410","notAllow":""}) 
    if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AS']):
        return jsonify({"rspCode":"500","notAllow":""}) 
    try:
        adminID = session.get('adminID')
    except:
        return jsonify({"rspCode":"500","notAllow":""}) 
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
    elif len(quota) > 2:
        notAllow.append("quota")
    if notAllow != []:
        #rspCode 401:有違法輸入
        return jsonify({"rspCode":"400","notAllow":notAllow})
    allotmentTime = str(datetime.datetime.now()).rsplit('.',1)[0]
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
                pointID = make_point()+"_{}".format(str(db.session.query(point).count() + 1))
                db.engine.execute(make_point_sql(pointID,adminID,userID))
                db.session.commit()
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
                    pointID = make_point()+"_{}".format(str(db.session.query(point).count() + 1))
                    db.engine.execute(make_point_sql(pointID,adminID,userID))
                    db.session.commit()
            return jsonify({"rspCode":"200","notAllow":""})
        except:
            return jsonify({"rspCode":"400","notAllow":"userID or adminID"})
    else:
        #kind錯誤
        return jsonify({"rspCode":"400","notAllow":"kind"})

#簡易個人配發紀錄
#要json傳userID
#回傳rspCode, period, frequency, quota, time
@Allotment.route("/simple_allotment_history", methods = ['POST'])
def simple_allotment_history():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","period":"","frequency":"","quota":"","time":""})
    try:
        try:
            json = request.get_json()
        except:
            return jsonify({"rspCode":"410","notAllow":""}) 
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AS']):
            return jsonify({"rspCode":"500","notAllow":""}) 
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
@Allotment.route('/allotment_history', methods = ['POST'])
def allotment_history():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","time":"","quota":"","period":"","frequency":"","userID":"","name":"","userSRRate":"","userSPRate":""})
    try:
        if not(session.get('userType') == userType['SA'] or session.get('userType') == userType['AS']):
            return jsonify({"rspCode":"500","time":"","quota":"","period":"","frequency":"","userID":"","name":"","userSRRate":"","userSPRate":""})
        try:
            json = request.get_json()
        except:
            return jsonify({"rspCode":"410","time":"","quota":"","period":"","frequency":"","userID":"","name":"","userSRRate":"","userSPRate":""})
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
