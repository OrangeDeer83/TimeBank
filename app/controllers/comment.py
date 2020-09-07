#coding:utf-8
from flask import Blueprint, session, jsonify, request
from ..models.model import *
from ..models.dao import *
from ..models import db, userType, noticeType
from sqlalchemy import or_
import os
import datetime
Comment = Blueprint('comment', __name__)


#評論資料顯示 SP、SR共用
#傳taskID
#回傳rspCode,userName,taskName
@Comment.route("/output/notice_comment", methods = ['POST'])
def output_notice_comment():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    try:
        userID_ = int(session('userID'))
    except:
        #尚未登入
        return jsonify({"rspCode":500})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500})
    json = request.get_json()
    taskID_ = json['taskID']
    try:
        task_= db.session.query(task).filter(taskID_ == task.taskID).first()
        if task_ == None :
            return jsonify({"rspCode":400,"taskName":"","userName":""})
    except:
        #taskID錯誤
        return jsonify({"rspCode":400,"taskName":"","userName":""})
    taskName = task_.taskName
    if task_.taskStatus in [3,6,7,8,13,14,15,16]:
        if task_.SR[0].userID != userID_:
            if task_.SP[0].userID != userID_:
                    #不是此task的SR或SP
                    return jsonify({"rspCode":402,"taskName":"","userName":""})
    else:
        #還不可評論
        return jsonify({"rspCode":403,"taskName":"","userName":""})
    try:
        userName = db.session.query(account.name).filter(account.userID == userID_).first()[0]
    except:
        #userID錯誤
        return jsonify({"rspCode":401,"taskName":"","userName":""})
    return jsonify({"rspCode":200,"taskName":taskName,"name":userName})

#評論
#傳taskID,comment,star
#回傳rspCode
@Comment.route("/comment_action", methods = ['POST'])
def comment_action():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500,"taskConflit":""})
    try:
        userID_ = int(session.get('userID'))
    except:
        return jsonify({"rspCode":500,"taskConflit":""})
    json = request.get_json()
    taskID_ = json['taskID']
    print(json)
    if not(json['star'] in ['1','2','3','4','5']):
        #star不合法
        return jsonify({"rspCode":403})
    user_comment =json['star'] + "," + json['comment']
    try:
        task_= db.session.query(task).filter(taskID_ == task.taskID).first()
        if task_ == None:
            return jsonify({"rspCode":400})
        elif task_.taskStatus not in [13,14,15,16,3,6,7,8]:
            return jsonify({"rspCode":400})
                
    except:
        #taskID錯誤
        return jsonify({"rspCode":400})
    if datetime.datetime.now() > task_.taskEndTime + datetime.timedelta(days=1) or datetime.datetime.now() < task_.taskStartTime:
        #不在可評價時間
        return jsonify({"rspCode":405})
    if task_.taskStatus in [3,6,7,8,13,14,15,16]: 
        if task_.SR[0].userID == int(userID_):   
                if task_.db_task_comment[0].commentStatus == -1:
                    comment_ = db.session.query(comment).filter(comment.taskID == taskID_).first()
                    comment_.SRComment = user_comment
                    if comment_.SPComment != None:
                        comment_.commentStatus = 0
                    db.session.commit()
                else:
                    #已經不可評論
                    return jsonify({"rspCode":404})
                return jsonify({"rspCode":200})
        if task_.SP[0].userID == int(userID_):    
            if task_.db_task_comment[0].commentStatus == -1:
                comment_ = db.session.query(comment).filter(comment.taskID == taskID_).first()
                comment_.SPComment = user_comment
                if comment_.SRComment != None:
                    comment_.commentStatus = 0
                db.session.commit()
            else:
                #已經不可評論
                return jsonify({"rspCode":404})
            return jsonify({"rspCode":200})
        else :
            #不是此task的SR或SP
            return jsonify({"rspCode":401})
    else:
        #此任務還不可評論
        return jsonify({"rspCode":402})

#GM審核評論頁面
#回傳commentList(taskStartTime, taskEndTime , taskName, taskConent, taskID, SRID, SRName, SRStar,SRConmment, SRPhone, SPID, SPName, SPStar, SPComment, SRPPhone)
@Comment.route("/GM/output/judge_comment_page", methods = ['GET'])
def GM_output_judge_comment_page():
    if request.method != 'GET':
        return jsonify({"rspCode":300})
    if session.get('userType') != userType['GM']:
        #此帳號不是GM
        return jsonify({"commentList":"","rspCode":500})
    comment_list = db.session.query(comment).filter(comment.commentStatus == 0).all()
    commentList = []
    try:
        for comment_ in comment_list:
            task_ = db.session.query(task).filter(task.taskID == comment_.taskID).first()
            if comment_.commentStatus == 0: 
                try:
                    SRStar = comment_.SRComment.split(',')[0]
                    SRComment = comment_.SRComment.split(',')[1]
                except:
                    SRStar = ""
                    SRComment = ""
                try:
                    SPStar = comment_.SPComment.split(',')[0]
                    SPComment = comment_.SPComment.split(',')[1]
                except:
                    SPStar = ""
                    SPComment = ""
                commentList.append({"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime),"taskName":task_.taskName\
                    ,"taskContent":task_.taskContent,"taskID":str(task_.taskID),"SRID":str(task_.SR[0].userID),"SRStar":SRStar\
                    ,"SRName":task_.SR[0].name,"SRComment":SRComment, "SPID":str(task_.SP[0].userID), "SPName":task_.SP[0].name\
                    , "SPStar":SPStar, "SPComment":SPComment,"SRPhone":task_.SR[0].userPhone,"SPPhone":task_.SP[0].userPhone})
        return jsonify({"commentList":commentList,"rspCode":200,"commentAmount":str(len(commentList))})
    except:
        return jsonify({"commentList":"","rspCode":400})

#審核評論
#傳taskID,status(0:否決, 1:確認)
#回傳rspCode
@Comment.route("/judge_commentaction", methods = ['POST'])
def judge_commentaction():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":500})
    try:
        json = request.get_json()
        taskID_ = int(json['taskID'])
        status = json['status']
    except:
        return jsonify({"rspCode":410})
    comment_ = db.session.query(comment).filter(comment.taskID == taskID_).first()
    if comment_ == None:
        #comment不存在
        return jsonify({"rspCode":400})
    elif comment_.commentStatus == -1:
        return jsonify({"rspCode":404})
    elif comment_.commentStatus != 0:
        return jsonify({"rspCode":403})
    if status == '0':
        SR_user = db.session.query(task).filter(task.taskID == taskID_).first().SR[0]
        SP_user = db.session.query(task).filter(task.taskID == taskID_).first().SP[0]
        comment_.commentStatus = 2
    elif status == '1':
        comment_.commentStatus = 1
        SR_user = db.session.query(task).filter(task.taskID == taskID_).first().SR[0]
        SP_user = db.session.query(task).filter(task.taskID == taskID_).first().SP[0]
        if comment_.SRComment != None:
            if SR_user.SRRate != None:
                SR_user.SRRate += int(comment_.SRComment.split(',')[0])
                SR_user.SRRateTimes +=1
            else:
                SR_user.SRRate = int(comment_.SRComment.split(',')[0])
                SR_user.SRRateTimes +=1
        if comment_.SPComment != None:
            if SP_user.SPRate != None:
                SP_user.SPRate += int(comment_.SPComment.split(',')[0])
                SP_user.SPRateTimes +=1
            else:
                SP_user.SPRate = int(comment_.SPComment.split(',')[0])
                SP_user.SPRateTimes +=1
    else:
        #status 只能0、1
        return jsonify({"rspCode":401})
    try:
        comment_.adminID = session.get('adminID')
        db.session.commit()
    except:
        return jsonify({"rspCode":402})
    notice_ = notice(userID = SR_user.userID,time = datetime.datetime.now(), status = noticeType['judgeComment'], haveRead = 0)
    db.session.add(notice_)
    db.session.commit()
    notice_task = noticeTask(noticeID = notice_.ID, taskID = comment_.taskID)
    db.session.add(notice_task)
    db.session.commit()
    notice_2 = notice(userID = SP_user.userID,time = datetime.datetime.now(), status = noticeType['judgeComment'], haveRead = 0)
    db.session.add(notice_2)
    db.session.commit()
    notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = comment_.taskID)
    db.session.add(notice_task_2)
    db.session.commit()
    return jsonify({"rspCode":200})

#評論歷史紀錄數量   md
#GET
#傳回rspCode,taskIDList
@Comment.route("/rate_history_list_amount", methods = ['GET'])
def rate_history_list_amount():
    if request.method != 'GET':
        return jsonify({"rspCode":30,"taskIDList":"","taskIDAmount":""})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":31,"taskIDList":"","taskIDAmount":""})
    try:
        taskIDList = []
        list_ = db.session.query(comment.taskID,comment.SRComment,comment.SPComment).filter(or_(comment.commentStatus == 2,comment.commentStatus == 1)).all()
        for commentID in list_:
            if commentID[1] != None or commentID[2] != None:  
                taskIDList.append(commentID[0])
        return jsonify({"rspCode":20,"taskIDList":taskIDList,"taskIDAmount":len(taskIDList)})
    except:
        return jsonify({"rspCode":48,"taskIDList":"","taskIDAmount":""})

#評論歷史紀錄 md 十個
#POST
#傳taskID
#傳回commentList(taskStartTime, taskEndTime , taskName, taskConent, taskID, SRID, SRName, SRStar,SRConmment, SRPhone, SPID, SPName, SPStar, SPComment, SRPPhone,gmID,approveResult)
@Comment.route("/rate_history_list", methods = ['POST'])
def rate_history_list():
    if request.method != 'POST':
        return jsonify({"rspCode":30})
    if session.get('userType') != userType['GM']:
        #此帳號不是GM
        return jsonify({"rspCode":31})
    try:
        json = request.get_json()
        taskID_ = int(json['taskID'])
    except:
        return jsonify({"rspCode":49})
    comment_list = db.session.query(comment).filter(or_(comment.commentStatus == 2,comment.commentStatus == 1)).filter(comment.taskID >= taskID_).limit(1).all()
    commentList = []
    try:
        for comment_ in comment_list:
            task_ = db.session.query(task).filter(task.taskID == comment_.taskID).first()
            try:
                SRStar = comment_.SRComment.split(',')[0]
                SRComment = comment_.SRComment.split(',')[1]
            except:
                SRStar = ""
                SRComment = ""
            try:
                SPStar = comment_.SPComment.split(',')[0]
                SPComment = comment_.SPComment.split(',')[1]
            except:
                SPStar = ""
                SPComment = ""
            return jsonify({"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime),"taskName":task_.taskName\
                ,"taskContent":task_.taskContent,"taskID":str(task_.taskID),"SRID":str(task_.SR[0].userID),"SRStar":SRStar\
                ,"SRName":task_.SR[0].name,"SRComment":SRComment, "SPID":str(task_.SP[0].userID), "SPName":task_.SP[0].name\
                , "SPStar":SPStar, "SPComment":SPComment,"SRPhone":task_.SR[0].userPhone,"SPPhone":task_.SP[0].userPhone,"gmID":str(comment_.adminID)\
                ,"approveResult":str(comment_.commentStatus),"rspCode":20})
    except:
        #資料有問題
        return jsonify({"rspCode":41})


