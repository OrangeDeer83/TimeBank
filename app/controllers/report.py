from flask import Blueprint, session, jsonify, request
from ..models.model import *
from ..models import db, userType
Report = Blueprint('report', __name__)
#檢舉動作
#POST
#傳reason,taskID
#return rspCode
@Report.route("/send_report", methods = ['POST'])
def send_report():
    if request.method != 'POST':
        return jsonify({"rspCode":"300"})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":"500"})
    try:
        userID_ = int(session.get('userID'))
    except:
        return jsonify({"rspCode":"500"})
    try:
        json = request.get_json()
        taskID_ = int(json['taskID'])
        reason_ = json['reportReason']
    except:
        return jsonify({"rspCode":"410"})
    task_ = db.session.query(task).filter(task.taskID == taskID_).first()
    if task_ == None:
        #沒有此task
        return jsonify({"rspCode":"401"})
    elif db.session.query(report).filter(report.reportUserID == userID_).filter(report.taskID == taskID_).first() != None:
        return jsonify({"rspCode":"404"})
    elif task_.SP[0].userID == userID_ or task_.SR[0].userID == userID_:
        if task_.taskStatus in [3,6,7,8,13,14,15,16]:
            newReport = report(taskID = taskID_, adminID = None, reason = reason_, reportStatus = 0, reportUserID = userID_)
            db.session.add(newReport)
            db.session.commit()
            return jsonify({"rspCode":"200"})
        #任務必須案過完成未完成才可檢舉
        return jsonify({"rspCode":"402"})
    else:
        #userID不是本任務相關人士
        return jsonify({"rspCode":"403"})
        
#審核檢舉
#POST
#傳reportID, reportStatus
#回傳rspCode
@Report.route("/approve", methods = ['POST'])
def approve():
    if request.method != 'POST':
        return jsonify({"rspCode":"300"})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":"500"})
    try:
        adminID_ = int(session.get('adminID'))
    except:
        return jsonify({"rspCode":"500"})
    adminID_ = 1
    try:
        json = request.get_json()
        reportID_ = json['reportID']
        reportStatus_ = int(json['reportStatus'])
    except:
        return jsonify({"rspCode":"410"})
    if db.session.query(adminAccount).filter(adminAccount.adminID == adminID_).first() == None:
        return jsonify({"rspCode":"404"}) 
    if not(reportStatus_ in [1,2]):
        #Status 不合法
        return jsonify({"rspCode":"403"})
    report_ = db.session.query(report).filter(report.reportID == reportID_).first()
    if report_ == None:
        #檢舉不存在
        return jsonify({"rspCode":"401"})
    elif report_.reportStatus != 0:
        #已經審理過
        return jsonify({"rspCode":"402"})
    else:
        report_.adminID = adminID_
        report_.reportStatus = reportStatus_ 
        db.session.commit()
        return jsonify({"rspCode":"200"})
    #未知
    return jsonify({"rspCode":"411"})

#全部有哪些report
#GET
#回傳rspCode, reportList
@Report.route("list_amount", methods = ['GET'])
def list_amount():
    if request.method != 'GET':
        return jsonify({"rspCode":"300","reportList":"","reportAmount":""})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":"500","reportList":"","reportAmount":""})
    try:
        report_list = db.session.query(report.reportID).filter(report.reportStatus == 0).all()
        reportList = []
        for report_ in report_list:
            reportList.append(report_[0])
        return jsonify({"rspCode":"200","reportList":reportList,"reportAmount":str(len(reportList))})
    except:
        return jsonify({"rspCode":"411","reportList":"","reportAmount":""})

@Report.route("list", methods = ['POST'])
def list():
    if request.method != 'POST':
        return jsonify({"reportList":"","rspCode":"300"})
    if session.get('userType') != userType['GM']:
        return jsonify({"reportList":"","rspCode":"500"})
    try:
        json = request.get_json()
        startID = int(json['reportID'])
    except:
        return jsonify({"reportList":"","rspCode":"410"})
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
            reportList.append({"taskName":task_.taskName,"taskContent":task_.taskContent,"SRRate":SRStar,"SRName":task_.SR[0].name,\
                                "SRComment":SRComment,"SRPhone":task_.SR[0].userPhone,"SPRate":SPStar,"SPName":task_.SP[0].name,\
                                "SPComment":SPComment,"SPPhone":task_.SP[0].userPhone})
        return jsonify({"reportList":reportList,"rspCode":"200"})
    except:
        return jsonify({"reportList":"","rspCode":"411"})

#檢舉審核紀錄數量
#POSR
#傳reportID
#回傳reporLisst,rspCode
@Report.route("report_history_list", methods = ['POST'])
def report_history_list():
    if request.method != 'POST':
        return jsonify({"rspCode":"300","reportList":"","reportAmount":""})
    if session.get('userType') != userType['GM']:
        return jsonify({"rspCode":"500","reportList":"","reportAmount":""})
    try:
        json = request.get_json()
        startID = int(json['reportID'])
    except:
        return jsonify({"reportList":"","rspCode":"410"})
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
                                "SRComment":SRComment,"SPRate":SPStar,"SPName":task_.SP[0].name,\
                                "SPComment":SPComment,"gmID":str(report_.adminID),"approveResult":str(report_.reportStatus)})
        return jsonify({"reportList":reportList,"rspCode":"200"})
    except:
        return jsonify({"reportList":"","rspCode":"411"})

@Report.route("report_history_list_amount", methods = ['GET'])
def report_history_list_amount():
    if request.method != 'GET':
        return jsonify({"rspCode":"300","reportList":"","reportAmount":""})
    #if session.get('userType') != userType['GM']:
    #    return jsonify({"rspCode":"500","reportList":"","reportAmount":""})
    try:
        report_list = db.session.query(report.reportID).filter(report.reportStatus != 0).all()
        reportList = []
        for report_ in report_list:
            reportList.append(report_[0])
        return jsonify({"rspCode":"200","reportList":reportList,"reportAmount":str(len(reportList))})
    except:
        return jsonify({"rspCode":"411","reportList":"","reportAmount":""})
