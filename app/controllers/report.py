#coding:utf-8
from flask import Blueprint, session, jsonify, request
from ..models.model import *
from ..models import db, userType,noticeType
Report = Blueprint('report', __name__)
#檢舉動作
#POST
#傳reason,taskID
#return rspCode
@Report.route("/send_report", methods = ['POST'])
def send_report():
    if request.method != 'POST':
        return jsonify({"rspCode":30})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":31})
    try:
        userID_ = int(session.get('userID'))
    except:
        return jsonify({"rspCode":31})
    try:
        json = request.get_json()
        taskID_ = int(json['taskID'])
        reason_ = json['reportReason']  
    except:
        return jsonify({"rspCode":49})
    task_ = db.session.query(task).filter(task.taskID == taskID_).first()
    if task_ == None:
        #沒有此task
        return jsonify({"rspCode":41})
    elif task_.SP[0].userID == userID_ or task_.SR[0].userID == userID_:
        if task_.taskStatus in [3,5,6,7,8,13,14,15,16]:
            newReport = report(taskID = taskID_, adminID = None, reason = reason_, reportStatus = 0, reportUserID = userID_,time_ = str(datetime.datetime.now()))
            db.session.add(newReport)
            db.session.commit()
            notice_ = notice(userID = userID_,time = str(datetime.datetime.now()), status = noticeType['sendReport'], haveRead = 0)
            db.session.add(notice_)
            db.session.commit()
            notice_report = noticeReport(noticeID = notice_.ID,reportID = newReport.reportID)
            db.session.add(notice_report)
            db.session.commit()
            return jsonify({"rspCode":20})
        #任務不可被檢舉
        return jsonify({"rspCode":42})
    else:
        #userID不是本任務相關人士
        return jsonify({"rspCode":43})
    
#審核檢舉
#POST
#傳reportID, reportStatus
#回傳rspCode
@Report.route("/approve", methods = ['POST'])
def approve():
    if request.method != 'POST':
        return jsonify({"rspCode":30})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":31})
    try:
        adminID_ = int(session.get('adminID'))
    except:
        return jsonify({"rspCode":31})
    try:
        json = request.get_json()
        reportID_ = json['reportID']
        reportStatus_ = int(json['reportStatus'])
    except:
        return jsonify({"rspCode":49})
    if db.session.query(adminAccount).filter(adminAccount.adminID == adminID_).first() == None: 
        return jsonify({"rspCode":44}) 
    if not(reportStatus_ in [1,2]):
        #Status 不合法
        return jsonify({"rspCode":43})
    report_ = db.session.query(report).filter(report.reportID == reportID_).first()
    if report_ == None:
        #檢舉不存在
        return jsonify({"rspCode":41})
    elif report_.reportStatus != 0:
        #已經審理過
        return jsonify({"rspCode":42})
    else:
        report_.adminID = adminID_
        report_.reportStatus = reportStatus_ 
        db.session.commit()
        notice_ = notice(userID = int(report_.account.userID),time = datetime.datetime.now(), status = noticeType['judgeReport'], haveRead = 0)
        db.session.add(notice_)
        db.session.commit()
        notice_report = noticeReport(noticeID = notice_.ID, reportID = report_.reportID)
        db.session.add(notice_report)
        db.session.commit()
        return jsonify({"rspCode":20})
    #未知
    return jsonify({"rspCode":48})

#全部有哪些report
#GET
#回傳rspCode, reportList
@Report.route("list_amount", methods = ['GET'])
def list_amount():
    if request.method != 'GET':
        return jsonify({"rspCode":30,"reportList":"","reportAmount":""})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":31,"reportList":"","reportAmount":""})
    try:
        report_list = db.session.query(report.reportID).filter(report.reportStatus == 0).all()
        reportList = []
        for report_ in report_list:
            reportList.append(report_[0])
        return jsonify({"rspCode":20,"reportList":reportList,"reportAmount":str(len(reportList))})
    except:
        return jsonify({"rspCode":48,"reportList":"","reportAmount":""})

@Report.route("/list", methods = ['POST'])
def list():
    if request.method != 'POST':
        return jsonify({"reportList":"","rspCode":30})
    if session.get('userType') != userType['GM']:
        return jsonify({"reportList":"","rspCode":31})
    try:
        json = request.get_json()
        startID = int(json['reportID'])
    except:
        return jsonify({"reportList":"","rspCode":49})
    try:
        report_list = db.session.query(report).filter(report.reportStatus == 0).filter(report.reportID == startID).all()
        reportList = []
        for report_ in report_list:
            task_ = report_.task
            comment_ = task_.db_task_comment[0]
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
            reportList.append({"taskName":task_.taskName,"taskContent":task_.taskContent,"SRRate":SRStar,"SRName":task_.SR[0].name,"reportTime":str(report_.time),\
                                "SRComment":SRComment,"SRPhone":task_.SR[0].userPhone,"SPRate":SPStar,"SPName":task_.SP[0].name,\
                                "SPComment":SPComment,"SPPhone":task_.SP[0].userPhone,"reportUserName":report_.account.name,\
                                "reportReason":report_.reason,"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime)})
        return jsonify({"reportList":reportList,"rspCode":20})
    except:
        return jsonify({"reportList":"","rspCode":48})

#檢舉審核紀錄
#POST
#傳reportID
#回傳reporLisst,rspCode
@Report.route("report_history_list", methods = ['POST'])
def report_history_list():
    if request.method != 'POST':
        return jsonify({"rspCode":30,"reportList":"","reportAmount":""})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":31,"reportList":"","reportAmount":""})
    try:
        json = request.get_json()
        startID = int(json['reportID'])
    except:
        return jsonify({"reportList":"","rspCode":49})
    try:
        report_list = db.session.query(report).filter(report.reportStatus != 0).filter(report.reportID == startID).all()
        reportList = []
        for report_ in report_list:
            task_ = report_.task
            comment_ = task_.db_task_comment[0]
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
            reportList.append({"taskName":task_.taskName,"taskContent":task_.taskContent,"SRRate":SRStar,"SRName":task_.SR[0].name,\
                                "SRComment":SRComment,"SRPhone":task_.SR[0].userPhone,"SPRate":SPStar,"SPName":task_.SP[0].name,\
                                "SPComment":SPComment,"SPPhone":task_.SP[0].userPhone,"gmID":str(report_.adminID),\
                                "approveResult":str(report_.reportStatus),"reportUserName":report_.account.name,\
                                "reportReason":report_.reason,"taskStartTime":str(task_.taskStartTime),\
                                "taskEndTime":str(task_.taskEndTime),"reportTime":str(report_.time)})
        return jsonify({"reportList":reportList,"rspCode":20})
    except:
        return jsonify({"reportList":"","rspCode":48})

@Report.route("report_history_list_amount", methods = ['GET'])
def report_history_list_amount():
    if request.method != 'GET':
        return jsonify({"rspCode":30,"reportList":"","reportAmount":""})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":31,"reportList":"","reportAmount":""})
    try:
        report_list = db.session.query(report.reportID).filter(report.reportStatus != 0).all()
        reportList = []
        for report_ in report_list:
            reportList.append(report_[0])
        return jsonify({"rspCode":20,"reportList":reportList,"reportAmount":str(len(reportList))})
    except:
        return jsonify({"rspCode":48,"reportList":"","reportAmount":""})
