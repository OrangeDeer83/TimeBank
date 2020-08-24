from flask import Blueprint, session, jsonify, request
from ..models.model import *
from ..models.dao import *
from ..models import db, userType
import os
import datetime
Comment = Blueprint('comment', __name__)


#評論資料顯示 SP、SR共用
#傳taskID
#回傳rspCode,userName,taskName
@Comment.route("/output/notice_comment", methods = ['POST'])
def output_notice_comment():
    if request.method != 'POST':
        return jsonify({"rspCode":"300"})
    try:
        userID_ = int(session('userID'))
    except:
        #尚未登入
        return jsonify({"rspCode":"403"})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":"500"})
    json = request.get_json()
    taskID_ = json['taskID']
    try:
        task_= db.session.query(task).filter(taskID_ == task.taskID).first()
        if task_ == None :
            return jsonify({"rspCode":"400","taskName":"","userName":""})
    except:
        #taskID錯誤
        return jsonify({"rspCode":"400","taskName":"","userName":""})
    taskName = task_.taskName
    if task_.taskStatus in [3,6,7,8]:
        if task_.SR[0].userID != userID_:
            if task_.SP[0].userID != userID_:
                    #不是此task的SR或SP
                    return jsonify({"rspCode":"402","taskName":"","userName":""})
    else:
        #還不可評論
        return jsonify({"rspCode":"403","taskName":"","userName":""})
    try:
        userName = db.session.query(account.userName).filter(account.userID == userID_).first()[0]
    except:
        #userID錯誤
        return jsonify({"rspCode":"401","taskName":"","userName":""})
    return jsonify({"rspCode":"200","taskName":taskName,"userName":userName})

#評論
#傳taskID,comment,star
#回傳rspCode
@Comment.route("/comment_action", methods = ['POST'])
def comment_action():
    if request.method != 'POST':
        return jsonify({"rspCode":"300"})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":"500","taskConflit":""})
    try:
        userID_ = int(session.get('userID'))
    except:
        return jsonify({"rspCode":"500","taskConflit":""})
    json = request.get_json()
    taskID_ = json['taskID']
    if not(json['star'] in ['1','2','3','4','5']):
        #star不合法
        return jsonify({"rspCode":"403"})
    user_comment =json['star'] + "," + json['comment']
    try:
        task_= db.session.query(task).filter(taskID_ == task.taskID).first()
        if task_ == None:
            return jsonify({"rspCode":"400"})
    except:
        #taskID錯誤
        return jsonify({"rspCode":"400"})
    if datetime.datetime.now() > task_.taskEndTime + datetime.timedelta(days=1) or datetime.datetime.now() < task_.taskEndTime:
        #不在可評價時間
        return jsonify({"rspCode":"405"})
    if task_.taskStatus in [3,6,7,8,13,14]: 
        if task_.SR[0].userID == int(userID_):   
                if task_.taskStatus == 14:
                    task_.taskStatus = 15
                    comment_ = db.session.query(comment).filter(comment.taskID == taskID_).first()
                    comment_.SRComment = user_comment
                    comment_.commentStatus = 0
                elif task_.taskStatus == 13:
                    #已經評論過
                    return jsonify({"rspCode":"404"})
                else:
                    task_.taskStatus = 13
                    comment_ = db.session.query(comment).filter(comment.taskID == taskID_).first()
                    comment_.SRComment = user_comment
                    comment_.commentStatus = -1
                    db.session.commit()
                return jsonify({"rspCode":"200"})
        if task_.SP[0].userID == int(userID_):    
            if task_.taskStatus == 13:
                task_.taskStatus = 15
                comment_ = db.session.query(comment).filter(comment.taskID == taskID_).first()
                comment_.SPComment = user_comment
                comment_.commentStatus = 0
                db.session.commit()
            elif task_.taskStatus == 14:
                #已經評論過
                return jsonify({"rspCode":"404"})
            else:
                comment_ = db.session.query(comment).filter(comment.taskID == taskID_).first()
                comment_.SPComment = user_comment
                comment_.commentStatus = -2
            db.session.commit()
            return jsonify({"rspCode":"200"})
        else :
            #不是此task的SR或SP
            return jsonify({"rspCode":"401"})
    else:
        #此任務還不可評論
        return jsonify({"rspCode":"402"})

#GM審核評論頁面
#回傳commentList(taskStartTime, taskEndTime , taskName, taskConent, taskID, SRID, SRName, SRStar,SRConmment, SRPhone, SPID, SPName, SPStar, SPComment, SRPPhone)
@Comment.route("/GM/output/judge_comment_page", methods = ['GET'])
def GM_output_judge_comment_page():
    if request.method != 'GET':
        return jsonify({"rspCode":"300"})
    if session.get('userType') != userType['GM']:
        #此帳號不是GM
        return jsonify({"commentList":"","rspCode":"500"})
    comment_list = db.session.query(comment).filter(comment.commentStatus == 0).all()
    commentList = []
    try:
        for comment_ in comment_list:
            task_ = db.session.query(task).filter(task.taskID == comment_.taskID).first()
            if task_.taskStatus == 15 and comment_.commentStatus == 0:
                commentList.append({"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime),"taskName":task_.taskName\
                    ,"taskContent":task_.taskContent,"taskID":str(task_.taskID),"SRID":str(task_.SR[0].userID),"SRStar":comment_.SRComment.split(',')[0]\
                    ,"SRName":task_.SR[0].name,"SRComment":comment_.SRComment.split(',')[1], "SPID":str(task_.SP[0].userID), "SPName":task_.SP[0].name\
                    , "SPStar":comment_.SPComment.split(',')[0], "SPComment":comment_.SPComment.split(',')[1],"SRPhone":task_.SR[0].userPhone,"SPPhone":task_.SP[0].userPhone})
            elif task_.taskStatus == 14 and comment_.commentStatus == 0:
                commentList.append({"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime),"taskName":task_.taskName\
                ,"taskContent":task_.taskContent,"taskID":str(task_.taskID),"SRID":str(task_.SR[0].userID),"SRStar":None\
                ,"SRName":task_.SR[0].name,"SRComment":None, "SPID":str(task_.SP[0].userID), "SPName":task_.SP[0].name\
                , "SPStar":comment_.SPComment.split(',')[0], "SPComment":comment_.SPComment.split(',')[1],"SRPhone":task_.SR[0].userPhone,"SPPhone":task_.SP[0].userPhone})
            elif task_.taskStatus == 13 and comment_.commentStatus == 0:
                commentList.append({"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime),"taskName":task_.taskName\
                    ,"taskContent":task_.taskContent,"taskID":str(task_.taskID),"SRID":str(task_.SR[0].userID),"SRStar":comment_.SRComment.split(',')[0]\
                    ,"SRName":task_.SR[0].name,"SRComment":comment_.SRComment.split(',')[1], "SPID":str(task_.SP[0].userID), "SPName":task_.SP[0].name\
                    , "SPStar":None, "SPComment":None,"SRPhone":task_.SR[0].userPhone,"SPPhone":task_.SP[0].userPhone})
        return jsonify({"commentList":commentList,"rspCode":"200","commentAmount":str(len(commentList))})
    except:
        return jsonify({"commentList":"","rspCode":"401"})

#審核評論
#傳taskID,status(0:否決, 1:確認)
#回傳rspCode
@Comment.route("/judge_commentaction", methods = ['POST'])
def judge_commentaction():
    if request.method != 'POST':
        return jsonify({"rspCode":"300"})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":"500"})
    try:
        json = request.get_json()
    except:
        return jsonify({"rspCode":"410"})
    taskID_ = json['taskID']
    status = json['status']
    comment_ = db.session.query(comment).filter(comment.taskID == taskID_).filter(comment.commentStatus == 0).first()
    if comment_ == None:
        #comment不存在或還不可檢查
        return jsonify({"rspCode":"400"})
    if status == '0':
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
        return jsonify({"rspCode":"401"})
    try:
        comment_.adminID = session.get('adminID')
        db.session.commit()
    except:
        return jsonify({"rspCode":"402"})
    return jsonify({"rspCode":"200"})




