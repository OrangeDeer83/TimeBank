#coding:utf-8
from flask import Blueprint, session, jsonify, request
from ..models.model import *
from ..models import db, userType,noticeType
from ..models.dao import *
import time
Task = Blueprint('task', __name__)


#取得SR歷史的任務
@Task.route('/SR/output/record', methods=['GET'])
def SR_output_record():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            if userID:
                try:
                    query_data = account.query.filter_by(userID = userID).first()
                    if query_data == None:
                        return jsonify({"rspCode": 401})                                   #沒有該帳號                                     #userID錯誤
                except:
                    return jsonify({"rspCode": 400})                                       #資料庫錯誤
                taskRecord = []
                for task in query_data.taskSR:
                    if task.taskStatus in [3, 5, 6, 7, 8]:
                        if task.db_task_comment[0].commentStatus in [1, 2]:
                            taskRecord.append(task)
                        elif task.taskStatus == 5:
                            taskRecord.append(task)
                    elif task.taskStatus in [4, 11]:
                        taskRecord.append(task)
                sortTaskByTaskID(taskRecord, 0, len(taskRecord) - 1)
                taskRecordJson = []
                for task in taskRecord:
                    if len(task.SP) == 0:
                        SPname = ""
                        SPID = ""
                    else:
                        SPname = task.SP[0].name
                        SPID = task.SP[0].userID
                    if len(task.db_task_comment) > 0:
                        if task.db_task_comment[0].SPComment == None:
                            SPScore = ""
                            SPComment = ""
                        else:
                            SPScore = task.db_task_comment[0].SPComment[0]
                            SPComment = task.db_task_comment[0].SPComment[2:]
                        if task.db_task_comment[0].SRComment == None:
                            SRScore = ""
                            SRComment = ""
                        else:
                            SRScore = task.db_task_comment[0].SRComment[0]
                            SRComment = task.db_task_comment[0].SRComment[2:]
                    else:
                        SPScore = ""
                        SPComment = ""
                        SRScore = ""
                        SRComment = ""
                    taskRecordJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSP": SPname, "taskSR": task.SR[0].name,\
                                            "SPComment": SPComment, "SPScore": SPScore, "SRComment": SRComment, "SPID":SPID,\
                                            "SRScore": SRScore})
                return jsonify({"rspCode": 200, "taskRecord": taskRecordJson})                    #成功取得
            else:
                return jsonify({"rspCode": 402})                                #沒有userID
        else:
            return jsonify({"rspCode": 500})                                    #權限不符
    else:
        return jsonify({"rspCode": 300})                                        #method使用錯誤

#取得SP已通過的任務
@Task.route('/SP/output/passed', methods=['GET'])
def SP_output_passed():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            if userID:
                try:
                    query_data = account.query.filter_by(userID = userID).first()
                    if query_data == None:
                        return jsonify({"rspCode": 401, "taskPassed": ""})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": 400, "taskPassed": ""})                                                  #資料庫錯誤
                taskPassed = []
                for task in query_data.taskSP:
                    if task.taskStatus in [2, 9, 10, 13, 14, 15, 16, 3, 6, 7, 8]:
                        if task.db_task_comment[0].commentStatus in [-1, 0]:
                            taskPassed.append(task)
                sortTaskByTaskID(taskPassed, 0, len(taskPassed) - 1)
                taskPassedJson = []
                for task in taskPassed:
                    commentStatus = 1
                    if task.db_task_comment[0].SPComment == None:
                        commentStatus = 0
                    taskStartTime = time.mktime(task.taskStartTime.timetuple()) * 1000
                    taskEndTime = time.mktime(task.taskEndTime.timetuple()) * 1000
                    print(taskStartTime)
                    print(taskEndTime)
                    taskPassedJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": taskStartTime, "taskEndTime": taskEndTime,\
                                            "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name,\
                                            "commentStatus": commentStatus, "SRID":task.SR[0].userID})
                return jsonify({"rspCode": 200, "taskPassed": taskPassedJson})                                        #成功取得
            else:
                return jsonify({"rspCode": 402})                                                    #沒有userID
        else:
            return jsonify({"rspCode": 500})                                                        #權限不符
    else:
        return jsonify({"rspCode": 300, "taskPassed": ""})                                                            #method使用錯誤

#取得SP審核中的任務
@Task.route('/SP/output/checking', methods=['GET'])
def SP_output_checking():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            if userID:
                try:
                    query_data = taskCandidate.query.filter_by(userID = userID).order_by(taskCandidate.taskID).all()
                    if query_data == None:
                        return jsonify({"rspCode": 401})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": 400})                                                  #資料庫錯誤
                taskChecking = []
                for candidate in query_data:
                    if candidate.task.taskStatus == 1:
                        taskChecking.append(candidate.task)
                sortTaskByTaskID(taskChecking, 0, len(taskChecking) - 1)
                taskCheckingJson = []
                for task in taskChecking:
                    taskCheckingJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSR": task.SR[0].name,"SRID":task.SR[0].userID})
                return jsonify({"rspCode": 200, "taskChecking": taskCheckingJson})                                        #成功取得
            else:
                return jsonify({"rspCode": 402})                                               #沒有userID
        else:
            return jsonify({"rspCode": 500})                                                    #權限不符
    else:
        return jsonify({"rspCode": 300})                                                      #method使用錯誤

#取得SP遭拒絕的任務
@Task.route('/SP/output/refused', methods=['GET'])
def SP_output_refused():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            if userID:
                try:
                    query_data = taskCandidate.query.filter_by(userID = userID).order_by(taskCandidate.taskID).all()
                    if query_data == None:
                        return jsonify({"rspCode": 401, "taskRefused": ""})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": 400, "taskRefused": ""})                                                  #資料庫錯誤
                taskRefused = []
                for candidate in query_data:
                    if candidate.task.taskStatus in [2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16] and candidate.task.SP[0].userID != userID:
                        taskRefused.append(candidate.task)
                sortTaskByTaskID(taskRefused, 0, len(taskRefused) - 1)
                taskRefusedJson = []
                for task in taskRefused:
                    taskRefusedJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name,\
                                            "SRID":task.SR[0].userID})
                return jsonify({"rspCode": 200, "taskRefused": taskRefusedJson})                                        #成功取得
            else:
                return jsonify({"rspCode": 402})                                #沒有userID
        else:
            return jsonify({"rspCode": 500})                                    #權限不符
    else:
        return jsonify({"rspCode": 300, "taskRefused": ""})                                                     #method使用錯誤

#取得SP歷史的任務
@Task.route('/SP/output/record', methods=['GET'])
def SP_output_record():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            if userID:
                try:
                    query_data = account.query.filter_by(userID = userID).first()
                    if query_data == None:
                        return jsonify({"rspCode": 401})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": 400})                                                  #資料庫錯誤
                taskRecord = []
                for task in query_data.taskSP:
                    if task.taskStatus in [3, 4, 5, 6, 7, 8]:
                        if task.db_task_comment[0].commentStatus in [1, 2]:
                            taskRecord.append(task)
                        elif task.taskStatus == 5:
                            taskRecord.append(task)
                    elif task.taskStatus == 11:
                        taskRecord.append(task)
                sortTaskByTaskID(taskRecord, 0, len(taskRecord) - 1)
                taskRecordJson = []
                for task in taskRecord:
                    if len(task.SP) == 0:
                        SPname = ""
                        SPID = ""
                    else:
                        SPname = task.SP[0].name
                        SPID = task.SP[0].userID
                    if len(task.db_task_comment) > 0:
                        if task.db_task_comment[0].SPComment == None:
                            SPScore = ""
                            SPComment = ""
                        else:
                            SPScore = task.db_task_comment[0].SPComment[0]
                            SPComment = task.db_task_comment[0].SPComment[2:]
                        if task.db_task_comment[0].SRComment == None:
                            SRScore = ""
                            SRComment = ""
                        else:
                            SRScore = task.db_task_comment[0].SRComment[0]
                            SRComment = task.db_task_comment[0].SRComment[2:]
                    else:
                        SPScore = ""
                        SPComment = ""
                        SRScore = ""
                        SRComment = ""
                    taskRecordJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSP": SPname, "taskSR": task.SR[0].name,\
                                            "SPComment": SPComment, "SPScore": SPScore, "SRComment": SRComment, "SRScore": SRScore,\
                                            "SPID": SPID, "SRID": task.SR[0].userID})
                return jsonify({"rspCode": 200, "taskRecord": taskRecordJson})                                        #成功取得
            else:
                return jsonify({"rspCode": 402})                                #沒有userID
        else:
            return jsonify({"rspCode": 500})                                    #權限不符
    else:
        return jsonify({"rspCode": 300})                                                     #method使用錯誤
#新增任務
#要json傳taskName,taskStartTime,taskEndTime,taskPoint,taskLocation,taskContent
#回傳rspCode,notAllow
@Task.route('/SR/add_task' , methods = ['POST'])
def SR_add_task():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500,"notAllow":"","taskConflit":"","pointConflit":""})
    try:
        json = request.get_json()
    except:
        return jsonify({"rspCode":410,"notAllow":"","taskConflit":"","pointConflit":""})
    try:
        userID_ = int(session.get('userID'))
    except:
        return jsonify({"rspCode":500,"notAllow":"","taskConflit":"","pointConflit":""})
    newTaskName = json['taskName']
    newTaskStartTime = json['taskStartTime']
    newTaskEndTime = json['taskEndTime']
    newTaskPoint = json['taskPoint']
    newTaskLocation = json['taskLocation']
    newTaskContent = json['taskContent']
    notAllow = []
    pointConflict= ''
    taskConflict= []
    if newTaskName == '' or len(newTaskName) > 20:
        notAllow.append("taskName")
    if newTaskStartTime == '':
        return jsonify({"rspCode":401,"notAllow":"","taskConflit":"","pointConflit":""})
    elif newTaskStartTime < str(datetime.datetime.now()):
        return jsonify({"rspCode":402,"notAllow":"","taskConflit":"","pointConflit":""})
    try:
        x=datetime.datetime.strptime(newTaskStartTime, "%Y-%m-%d %H:%M:%S")
        y=datetime.datetime.strptime(newTaskEndTime, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(minutes = 1)
        if newTaskEndTime == '':
            return jsonify({"rspCode":401,"notAllow":"","taskConflit":"","pointConflit":""})
        elif x >= y:
            return jsonify({"rspCode":401,"notAllow":"","taskConflit":"","pointConflit":""})
    except:
        return jsonify({"rspCode":401,"notAllow":"","taskConflit":"","pointConflit":""})
    if not(newTaskPoint.isdigit()):
        notAllow.append("taskPoint")
    elif len(newTaskPoint) > 2:
        notAllow.append("taskPoint")
    elif int(newTaskPoint) < 0:
        notAllow.append("taskPoint")
    if newTaskLocation == '':
        notAllow.append("taskLocation")
    if userID_ == '':
        notAllow.append("userID")
    userAllPoint=0
    user = db.session.query(account).filter(account.userID == userID_).first()
    #身為SR有沒有時間和point
    userTaskSR =user.taskSR
    if userTaskSR != []:
        for userTaskSR_ in userTaskSR:
            if not(userTaskSR_.taskStatus == 0 or userTaskSR_.taskStatus == 1 or userTaskSR_.taskStatus == 2):
                continue
            userAllPoint+=userTaskSR_.taskPoint
            if not(str(userTaskSR_.taskStartTime) > newTaskEndTime or str(userTaskSR_.taskEndTime) < newTaskStartTime):
                taskConflict.append({"taskID":"{}".format(userTaskSR_.taskID),"taskName":"{}".format(userTaskSR_.taskName)})
    #身為SP有沒有時間
    userTaskSP =user.taskSP
    if userTaskSP != []:
        for userTaskSP_ in userTaskSP:
            if not(userTaskSP_.taskStatus == 0 or userTaskSP_.taskStatus == 1 or userTaskSP_.taskStatus == 2):
                continue
            if not(str(userTaskSP_.taskStartTime) > newTaskEndTime or str(userTaskSP_.taskEndTime) < newTaskStartTime):
                taskConflict.append({"taskID":"{}".format(userTaskSP_.taskID),"taskName":"{}".format(userTaskSP_.taskName)})
    #身為候選人有沒有時間
    userCandidate = user.db_account_taskCandidate
    for userCandidate_ in userCandidate:    
        task_ = userCandidate_.task
        if not(task_.taskStatus == 0 or task_.taskStatus == 1):
            continue
        if not(str(task_.taskStartTime) > newTaskEndTime or str(task_.taskEndTime) < newTaskStartTime):
                taskConflict.append({"taskID":"{}".format(task_.taskID),"taskName":"{}".format(task_.taskName)})
    if userAllPoint+ int(newTaskPoint) > db.session.query(account.userPoint).filter(account.userID == userID_).first()[0]:
        pointConflict = ("-{}".format(userAllPoint + int(newTaskPoint) - db.session.query(account.userPoint).filter(account.userID == userID_).first()[0]))
    if notAllow != [] or taskConflict != []:
        return jsonify({"rspCode":400,"notAllow":notAllow,"taskConflit":taskConflict,"pointConflit":""})
    elif  pointConflict != '':
          return jsonify({"rspCode":403,"notAllow":"","taskConflit":"","pointConflit":pointConflict})
    addTask = task(taskContent= newTaskContent,taskName=newTaskName ,taskStartTime= newTaskStartTime,taskEndTime = newTaskEndTime,taskPoint = newTaskPoint,taskLocation = newTaskLocation ,taskStatus = 0)
    SR = db.session.query(account).filter(account.userID == userID_).first()
    addTask.SR=[SR]
    db.session.add(addTask) 
    db.session.commit()
    comment_ = comment(taskID = addTask.taskID, SRComment = None, SPComment = None, commentStatus = -1, adminID = None)
    db.session.add(comment_)
    db.session.commit()
    task_ID = addTask.taskID
    EndTime = str(addTask.taskEndTime + datetime.timedelta(minutes=1))
    db.engine.execute(task_status_4_dead_line(task_ID,newTaskStartTime))
    db.engine.execute(thing_will_do_while_task_endTime_plus_1h(task_ID,EndTime))
    EndTime = str(addTask.taskEndTime + datetime.timedelta(hours = 24))
    db.engine.execute(comment_status_0(task_ID,EndTime))
    #notice 
    notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['createTask'], haveRead = 0)
    db.session.add(notice_)
    db.session.commit()
    notice_task = noticeTask(noticeID = notice_.ID, taskID = task_ID)
    db.session.add(notice_task)
    db.session.commit()
    db.engine.execute(NoSP(userID_,task_ID,str(addTask.taskStartTime + datetime.timedelta(seconds=3))))
    return jsonify({"rspCode":200,"notAllow":"","taskConflit":"","pointConflit":""})
##顯示可接任務
#回傳taskName, taskStartTime, taskEndTime, taskPoint, SRName,taskLocation,taskContent
@Task.route('/SP/output/task_can_be_taken', methods = ['GET'])
def SP_output_task_can_be_taken():
    if request.method != 'GET':
        return jsonify({"rspCode":300,"taskList":""})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500,"taskList":""})
    try:
        userID = int(session.get('userID'))
    except:
        return jsonify({"rspCode":500,"taskList":""})
    taskName = []
    taskStartTime = []
    taskEndTime = []
    taskPoint = []
    SRName = []
    taskLocation = []
    taskContent = []
    taskID = []
    task_list=[]
    taskData = db.session.query(task).filter(task.taskStatus.in_([0,1])).order_by(task.taskStartTime,task.taskPoint.desc()).all()
    for task_ in taskData:
        #flag = 0
        #檢查是不是自己發的
        if task_.SR[0].userID == userID:
            continue
        #檢查接過了沒
        elif db.session.query(taskCandidate.userID).filter(task_.taskID==taskCandidate.taskID).all() != None:
            for source in db.session.query(taskCandidate.userID).filter(task_.taskID==taskCandidate.taskID).all():
                if source[0] == userID:
                    continue
        task_list.append({"taskID":str(task_.taskID),"taskName":task_.taskName,"taskStartTime":str(task_.taskStartTime),\
                        "taskEndTime":str(task_.taskEndTime),"taskPoint":str(task_.taskPoint),"SRName":task_.SR[0].name,\
                        "taskLocation":task_.taskLocation,"taskContent":task_.taskContent,"SRID":task_.SR[0].userID})
    return ({"rspCode":200,"taskList":task_list})
#承接接任務
#用json傳taskID
#回傳rspCode,taskConflit
@Task.route("/SP/taken_task" , methods = ['POST'])
def SP_taken_task():
    if request.method != 'POST':
        return jsonify({"rspCode":300,"taskConflit":""})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500,"taskConflit":""})
    try:
        userID = int(session.get('userID'))
    except:
        return jsonify({"rspCode":500,"taskConflit":""})
    try:
        try:
            json = request.get_json()
        except:
            return jsonify({"rspCode":410,"taskConflit":""})
        try:
            taskID_ = int(json['taskID'])
        except:
            return jsonify({"rspCode":403,"taskConflit":""})
        if db.session.query(taskCandidate.userID).filter(taskID_==taskCandidate.taskID ).filter(userID==taskCandidate.userID ).all() != []:
            #已經申請此任務
            return jsonify({"rspCode":401,"taskConflit":""})
        if db.session.query(task).filter(task.taskID == taskID_).first() == None:
            #任務不存在
            return jsonify({"rspCode":403,"taskConflit":""})
        task_ = db.session.query(task).filter(task.taskID == taskID_).filter(task.taskStatus.in_([0,1])).first()
        if task_ == None:
            #此任務已有SP
            return jsonify({"rspCode":402,"taskConflit":""})
        if task_.SR[0].userID == userID:
            #自己的
            return({"rspCode":405,"taskConflit":""})
        user = db.session.query(account).filter(account.userID == userID).first()
        userTaskSR =user.taskSR
        if userTaskSR != []:
            for userTaskSR_ in userTaskSR:
                if not(userTaskSR_.taskStatus == 0 or userTaskSR_.taskStatus == 1 or userTaskSR_.taskStatus == 2):
                    continue
                if not(str(userTaskSR_.taskStartTime) > str(task_.taskEndTime) or str(userTaskSR_.taskEndTime) < str(task_.taskStartTime)):
                    return jsonify({"rspCode":404,"taskConflit":{"taskID":str(userTaskSR_.taskID),"taskName":userTaskSR_.taskName}})
        userTaskSP = user.taskSP
        if userTaskSP != []:
            for userTaskSP_ in userTaskSP:
                if not(userTaskSP_.taskStatus == 0 or userTaskSP_.taskStatus == 1 or userTaskSP_.taskStatus == 2):
                    continue
                if not(str(userTaskSP_.taskStartTime) > str(task_.taskEndTime) or str(userTaskSP_.taskEndTime) < str(task_.taskStartTime)):
                    return jsonify({"rspCode":404,"taskConflit":{"taskID":str(userTaskSP_.taskID),"taskName":userTaskSP_.taskName}})
        userCandidate = user.db_account_taskCandidate
        for userCandidate_ in userCandidate:    
            userCandidateTask = userCandidate_.task
            if not(userCandidateTask.taskStatus == 0 or userCandidateTask.taskStatus == 1):
                continue
            if not(str(userCandidateTask.taskStartTime) > str(task_.taskEndTime) or str(userCandidateTask.taskEndTime) < str(task_.taskStartTime)):
                return jsonify({"rspCode":404,"taskConflit":{"taskID":str(userCandidateTask.taskID),"taskName":userCandidateTask.taskName}})
        task_.taskStatus = 1
        taskCandidateAdd = taskCandidate(taskID=taskID_,userID=userID)
        db.session.add(taskCandidateAdd)
        db.session.commit()
        notice_ = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['haveCandidate'], haveRead = 0)
        db.session.add(notice_)
        db.session.commit()
        notice_candidate = noticeCandidate(noticeID = notice_.ID, candidateID = taskCandidateAdd.rejectID)
        db.session.add(notice_candidate)
        db.session.commit()
        return jsonify({"rspCode":200,"taskConflit":""})
    except:
        return jsonify({"rspCode":400,"taskConflit":""})

#顯示雇主已發布任務
#回傳taskName, taskStartTime, taskEndTime, taskPoint, taskCandidate,taskLocation,taskContent, taskID 變get
#candidate前面是name後面是id
@Task.route("/SR/output/passed", methods = ['GET'])
def SR_passed():
    if request.method != 'GET':
        return jsonify({"rspCode":300,"taskList":"","taskAmount":""})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500,"taskConflit":""})
    try:
        userID_ = int(session.get('userID'))
    except:
        return jsonify({"rspCode":500,"taskConflit":""})
    try:
        task_list = []
        task_list_ = db.session.query(account).filter(account.userID == userID_).first().taskSR
        task_has_candidate = []
        task_no_candidate = []
        for task_ in task_list_:
            if task_.db_task_taskCandidate != []:
                task_has_candidate.append(task_)
            else:
                task_no_candidate.append(task_)
        sortTaskByTaskStartTime(task_has_candidate, 0, len(task_has_candidate) - 1)
        sortTaskByTaskStartTime(task_no_candidate, 0 ,len(task_no_candidate) - 1)
        for task_ in task_has_candidate:
            if task_.taskStatus in [0,1]:
                candidateList = db.session.query(account.name,account.userID).join(taskCandidate).filter(taskCandidate.taskID == task_.taskID and taskCandidate.userID == account.userID).all()
                candidateNum = len(candidateList)
                task_list.append({"taskID":str(task_.taskID),"taskName":task_.taskName,"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime),"taskStatus":str(task_.taskStatus)\
                                ,"taskPoint":str(task_.taskPoint),"taskContent":task_.taskContent,"taskLocation":task_.taskLocation,"CandidateList":candidateList,"cadidateAmount":str(candidateNum)})
        for task_ in task_no_candidate:
            if task_.taskStatus in [0,1]:
                candidateList = db.session.query(account.name,account.userID).join(taskCandidate).filter(taskCandidate.taskID == task_.taskID and taskCandidate.userID == account.userID).all()
                candidateNum = len(candidateList)
                task_list.append({"taskID":str(task_.taskID),"taskName":task_.taskName,"taskStartTime":str(task_.taskStartTime),"taskEndTime":str(task_.taskEndTime),"taskStatus":str(task_.taskStatus)\
                                ,"taskPoint":str(task_.taskPoint),"taskContent":task_.taskContent,"taskLocation":task_.taskLocation,"CandidateList":candidateList,"cadidateAmount":str(candidateNum)})

        return jsonify({"rspCode":200,"taskList":task_list,"taskAmount":str(len(task_list))})
    except: 
        return jsonify({"rspCode":400,"taskList":"","taskAmount":""})   

#編輯任務
#傳 taskID,taskName,taskStartTime,taskEndTime,taskPoint,taskLocation,taskContent
#回傳rspCode
@Task.route("/SR/edit_task", methods = ['POST'])
def SR_edit_task():
    if request.method != 'POST':
        return jsonify({"rspCode":30,"notAllow":"","taskConflit":"","pointConflit":""})
    try:
        userID_ = int(session.get('userID'))
    except:
        #尚未登入
        return jsonify({"rspCode":31,"notAllow":"","taskConflit":"","pointConflit":""})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":31,"notAllow":"","taskConflit":"","pointConflit":""})
    try:
        json = request.get_json()
    except:
        return jsonify({"rspCode":49,"notAllow":"","taskConflit":"","pointConflit":""})
    print(json)
    taskID_ = json['taskID']
    task_taeget = db.session.query(task).filter(task.taskID == int(taskID_),task.taskStatus == 0).first()
    if db.session.query(task).filter(task.taskID == int(taskID_)).first() == None:
        #此任務不存在
        return jsonify({"rspCode":40,"notAllow":"","taskConflit":"","pointConflit":""})
    oldTask = db.session.query(task).filter(task.taskID == int(taskID_),task.taskStatus == 0).first()
    if oldTask == None:
        #任務已有人申請或狀態不核准
        return ({"rspCode":41,"notAllow":"","taskConflit":"","pointConflit":""})
    json = request.get_json()
    newTaskName = json['taskName']
    newTaskStartTime = json['taskStartTime']
    newTaskEndTime = json['taskEndTime']
    newTaskPoint = json['taskPoint']
    newTaskLocation = json['taskLocation']
    newTaskContent = json['taskContent']
    notAllow = []
    pointConflict= ''
    taskConflict= []
    if len(newTaskName) > 20:
        notAllow.append("taskName")
    if newTaskStartTime == '':
        newTaskStartTime = str(oldTask.taskStartTime)
    if newTaskEndTime == '':
        newTaskEndTime = str(oldTask.taskEndTime)
    if newTaskStartTime != '':
        if newTaskStartTime < str(datetime.datetime.now()):
            return ({"rspCode":44,"notAllow":"","taskConflit":"","pointConflit":""})
    try:
        if len(newTaskStartTime) != 19 or len(newTaskEndTime) != 19:
            return ({"rspCode":43,"notAllow":"","taskConflit":"","pointConflit":""})
        x=datetime.datetime.strptime(newTaskStartTime, "%Y-%m-%d %H:%M:%S")
        y=datetime.datetime.strptime(newTaskEndTime, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(minutes = 1)
        if newTaskEndTime != '':
            if x >= y:
                return ({"rspCode":44,"notAllow":"","taskConflit":"","pointConflit":""})
    except:
        return ({"rspCode":43,"notAllow":"","taskConflit":"","pointConflit":""})
    if not(newTaskPoint.isdigit()):
        notAllow.append("taskPoint")
    elif len(newTaskPoint) > 2:
        notAllow.append("taskPoint")
    elif int(newTaskPoint) < 0:
        notAllow.append("taskPoint")
    if userID_ == '':
        notAllow.append("userID")
    elif userID_ != oldTask.SR[0].userID:
        notAllow.append("userID")
    userAllPoint = 0
    user = db.session.query(account).filter(account.userID == userID_).first()
    #身為SR有沒有時間和point
    userTaskSR =user.taskSR
    if userTaskSR != []:
        for userTaskSR_ in userTaskSR:
            if userTaskSR_.taskID ==int(taskID_):
                continue
            if not(userTaskSR_.taskStatus == 0 or userTaskSR_.taskStatus == 1 or userTaskSR_.taskStatus == 2):
                continue
            userAllPoint+=userTaskSR_.taskPoint
            if not(str(userTaskSR_.taskStartTime) > str(newTaskEndTime) or str(userTaskSR_.taskEndTime) < str(newTaskStartTime)):
                taskConflict.append({"taskID":str(userTaskSR_.taskID),"taskName":userTaskSR_.taskName})
    #身為SP有沒有時間
    userTaskSP =user.taskSP
    if userTaskSP != []:
        for userTaskSP_ in userTaskSP:
            if not(userTaskSP_.taskStatus == 0 or userTaskSP_.taskStatus == 1 or userTaskSP_.taskStatus == 2):
                continue
            if not(str(userTaskSP_.taskStartTime) > str(newTaskEndTime) or str(userTaskSP_.taskEndTime) < str(newTaskStartTime)):
                taskConflict.append({"taskID":str(userTaskSP_.taskID),"taskName":userTaskSP_.taskName})
    #身為候選人有沒有時間
    userCandidate = user.db_account_taskCandidate
    for userCandidate_ in userCandidate:    
        task_ = userCandidate_.task
        if not(task_.taskStatus == 0 or task_.taskStatus == 1):
            continue
        if not(str(task_.taskStartTime) > str(newTaskEndTime) or str(task_.taskEndTime) < str(newTaskStartTime)):
            taskConflict.append({"taskID":str(task_.taskID),"taskName":task_.taskName})
    if userAllPoint+ int(newTaskPoint) > db.session.query(account.userPoint).filter(account.userID == userID_).first()[0]:
        pointConflict = ("-{}".format(str(userAllPoint + int(newTaskPoint) - db.session.query(account.userPoint).filter(account.userID == userID_).first()[0])))
    if notAllow != [] or taskConflict != []:
        #有不合法輸入
        return jsonify({"rspCode":42,"notAllow":notAllow,"taskConflit":taskConflict,"pointConflit":""})
    elif  pointConflict != '':
         return jsonify({"rspCode":45,"notAllow":"","taskConflit":"","pointConflit":pointConflict})
    if newTaskContent != "":
        oldTask.taskContent = newTaskContent
    if newTaskName != "":
        oldTask.taskName = newTaskName
    if newTaskStartTime != "":
        x =  datetime.datetime.strptime(newTaskStartTime[:19], "%Y-%m-%d %H:%M:%S")
        oldTask.taskStartTime = x
    if newTaskEndTime != "":
        x =  datetime.datetime.strptime(newTaskEndTime[:19], "%Y-%m-%d %H:%M:%S")
        oldTask.taskEndTime = x
    if newTaskLocation != "":
        oldTask.taskLocation = newTaskLocation
    if newTaskPoint != "":
        oldTask.taskPoint = newTaskPoint
    db.session.commit()
    notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['editTask'], haveRead = 0)
    db.session.add(notice_)
    db.session.commit()
    notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
    db.session.add(notice_task)
    db.session.commit()
    EndTime = str(oldTask.taskEndTime + datetime.timedelta(minutes=1))
    db.engine.execute(drop_task_status_4_dead_line(taskID_))
    db.engine.execute(task_status_4_dead_line(taskID_,oldTask.taskStartTime))
    db.engine.execute(drop_thing_will_do_while_task_endTime_plus_1h(taskID_))
    db.engine.execute(thing_will_do_while_task_endTime_plus_1h(taskID_,EndTime))
    EndTime = str(oldTask.taskEndTime + datetime.timedelta(minutes=3))
    db.engine.execute(drop_comment_status_0(taskID_))
    db.engine.execute(comment_status_0(taskID_,EndTime))
    db.engine.execute(drop_NoSP(taskID_,userID_))
    db.engine.execute(NoSP(userID_,taskID_,str(oldTask.taskStartTime + datetime.timedelta(seconds=3))))
    return jsonify({"rspCode":20})
#雇主確定雇員
#傳cnadidateID,taskID
#回傳rspCode
@Task.route("/SR/decide_SP", methods = ["POST"])
def SR_decide_SP():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500,"taskConflit":""})
    try:
        userID = int(session.get('userID'))
    except:
        return jsonify({"rspCode":500,"taskConflit":""})
    try:
        json = request.get_json()
        candidateID_ = json['candidateID']
        taskID_ = json['taskID']
        flag = 0
        task_ = db.session.query(task).filter(task.taskID == taskID_).first()
        if str(datetime.datetime.now()) > str(task_.taskStartTime):
            #任務時間超過
            return jsonify({"rspCode":403}) 
        if userID != task_.SR[0].userID:
            return jsonify({"rspCode":402})
        for people in task_.db_task_taskCandidate:
            if people.userID == int(candidateID_):
                flag = 1
        if flag == 0:
            #此人不是候選人
            return jsonify({"rspCode":401})
        if not(task_.taskStatus == 1 or task_.taskStatus == 0):
            return jsonify({"rspCode":403})
        task_.taskStatus = 2
        SP_ = db.session.query(account).filter(account.userID == candidateID_).first()
        task_.SP = [SP_]
        db.session.commit()
        notice_ = notice(userID = candidateID_,time = datetime.datetime.now(), status = noticeType['SPPassed'], haveRead = 0)
        db.session.add(notice_)
        db.session.commit()
        notice_task = noticeTask(noticeID = notice_.ID, taskID = task_.taskID)
        db.session.add(notice_task)
        db.session.commit()
        db.engine.execute(task_will_start(task_.SR[0].userID,task_.taskID,str(task_.taskStartTime - datetime.timedelta(hours = 1)),task_.SP[0].userID))
        db.engine.execute(task_start(task_.SR[0].userID,task_.taskID,task_.taskStartTime,task_.SP[0].userID))	
        db.engine.execute(plzComment(task_.SR[0].userID,task_.taskID,str(task_.taskEndTime + datetime.timedelta(hours = 23)),task_.SP[0].userID))
        db.engine.execute(taskEndTime_sql(task_.SR[0].userID,task_.taskID,str(task_.taskEndTime),task_.SP[0].userID))
        print(taskID_ , candidateID_ )
        return jsonify({"rspCode":200})
    except:
        return jsonify({"rspCode":400})
#雇主已接受
#回傳taskName, taskStartTime, taskEndTime, taskPoint, SPName,taskLocation,taskContent, taskID在taskList,rspCode,taskAmount
@Task.route("/SR/output/accept", methods = ['GET'])
def SR_accept():
    try:
        if request.method != 'GET':
            return jsonify({"rspCode":300,"taskList":"","taskAmount":""})
        if session.get('userType') != userType['USER']:
            return jsonify({"rspCode":500,"taskList":"","taskAmount":""})
        try:
            SRID = int(session.get('userID'))
        except:
            return jsonify({"rspCode":500,"taskList":"","taskAmount":""})
        task_list = db.session.query(account).filter(account.userID == SRID).first().taskSR
        taskList = []
        sortTaskByTaskStartTime(taskList,0,len(taskList))
        for task_ in task_list:
            if task_.taskStatus in  [2,9,3,6,7,8,10,13,14,15,16]:
                if task_.taskEndTime + datetime.timedelta(hours=24) > datetime.datetime.now():
                    if task_.db_task_comment[0].commentStatus in [-1, 0]:
                        commentStatus = 1
                        if task_.db_task_comment[0].SRComment == None:
                            commentStatus = 0
                        taskStartTime = time.mktime(task_.taskStartTime.timetuple()) * 1000
                        taskEndTime = time.mktime(task_.taskEndTime.timetuple()) * 1000
                        taskList.append({"taskName":task_.taskName,"taskStartTime": taskStartTime,"taskEndTime": taskEndTime,\
                                        "taskPoint":str(task_.taskPoint),"taskSPName":task_.SP[0].name,"taskLocation":task_.taskLocation,\
                                        "taskContent":task_.taskContent,"taskID":str(task_.taskID),"taskStatus":str(task_.taskStatus),\
                                        "commentStatus": commentStatus,"SPID":task_.SP[0].userID})
        return jsonify({"rspCode":200,"taskList":taskList,"taskAmount":str(len(taskList))})
    except:
        return jsonify({"rspCode":400,"taskList":"","taskAmount":""})

#雇主刪除任務
#傳taskID
#回傳rspCode
@Task.route("/SR/delete_task",methods = ['POST'])
def delete_task():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    json = request.get_json()
    taskID_ =json['taskID']
    try:
        userID_ = str(session.get('userID'))
    except:
        #尚未登入
        return jsonify({"rspCode":500})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500})
    task_ = db.session.query(task).filter(taskID_ == task.taskID).first()
    if task_ == None:
        #任務不存在
        return jsonify({"rspCode":400})
    if not(userID_.isdigit()):
        #session userID 有問題
        return jsonify({"rspCode":403})
    if int(userID_) != db.session.query(task).filter(task.taskID == taskID_).first().SR[0].userID:
        #任務發放人不是你不能刪除
        return jsonify({"rspCode":401})
    if not(task_.taskStatus == 0 or task_.taskStatus == 1):
        #只有在任務沒被任何人申請過的階段才能刪除
        return jsonify({"rspCode":402})
    task_.taskStatus = 12
    db.session.commit()
    notice_ = notice(userID = int(userID_),time = datetime.datetime.now(), status = noticeType['deleteTask'], haveRead = 0)
    db.session.add(notice_)
    db.session.commit()
    notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
    db.session.add(notice_task)
    db.session.commit()
    db.engine.execute(drop_thing_will_do_while_task_endTime_plus_1h(str(taskID_)))
    db.engine.execute(drop_task_status_4_dead_line(str(taskID_)))
    db.engine.execute(drop_comment_status_0(str(taskID_)))
    notice_task_list = db.session.query(task).filter(task.taskID == taskID_).first().db_task_noticeTask
    for notice_task in notice_task_list:
        if notice_task.notice.status == 1:
            notice_delete = notice_task.notice
            db.session.delete(noticeTask)
            db.session.commit()
            db.session.delete(notice_delete)
    return jsonify({"rspCode":200})

#雇主取消
#傳taskID
#回傳rspCode
@Task.route("/SR/cancel_task", methods = ['POST'])
def SR_cancel_task():
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
    task_ = db.session.query(task).filter(task.taskID == taskID_).first()
    if task_ == None:
        #任務不存在
        return jsonify({"rspCode":400})
    elif str(task_.taskStartTime) < str(datetime.datetime.now()):
        return ({"rspCode":"402"})
    elif task_.SR[0].userID != userID_:
        #你不是任務發布人
        return jsonify({"rspCode":401})
    elif task_.taskStatus == 2:
        task_.taskStatus = 9
        db.session.commit()
        notice_ = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['SRCancel'], haveRead = 0)
        db.session.add(notice_)
        db.session.commit()
        notice_task = noticeTask(noticeID = notice_.ID, taskID = task_.taskID)
        db.session.add(notice_task)
        db.session.commit()
        return jsonify({"rspCode":200})
    elif task_.taskStatus == 10:
        task_.taskStatus = 11
        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['cancelTask'], haveRead = 0)
        db.session.add(notice_)
        db.session.commit()
        notice_task = noticeTask(noticeID = notice_.ID, taskID = task_.taskID)
        db.session.add(notice_task)
        db.session.commit()
        notice_2 = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['cancelTask'], haveRead = 0)
        db.session.add(notice_2)
        db.session.commit()
        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = task_.taskID)
        db.session.add(notice_task_2)
        db.session.commit()
        db.engine.execute(drop_plzComment(taskID_))
        db.engine.execute(drop_taskEndTime_sql(taskID_))
        return jsonify({"rspCode":200})
    #任務不可取消
    return jsonify({"rspCode":402})
#雇員取消
#傳taskID
#回傳rspCode
@Task.route("/SP/cancel_task", methods = ["POST"])
def SP_cancel_task():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    try:
        userID_ = int(session.get('userID'))
    except:
        #尚未登入
        return jsonify({"rspCode":500})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500})
    json = request.get_json()
    taskID_ = json['taskID']
    task_ = db.session.query(task).filter(task.taskID == taskID_).first()   
    if task_ == None:
        #任務不存在
        return jsonify({"rspCode":400})
    elif str(task_.taskStartTime) < str(datetime.datetime.now()):
        return ({"rspCode":402})
    elif task_.SP == []:
        try:
            candidateList =task_.db_task_taskCandidate
            for candidate in candidateList:
                if candidate.userID == int(userID_):
                    target = db.session.query(taskCandidate).filter(taskCandidate.userID == int(userID_)).filter(taskCandidate.taskID == taskID_).first()
                    noticeCandidate_ = db.session.query(noticeCandidate).filter(noticeCandidate.candidateID == target.rejectID).first()
                    notice__ = db.session.query(notice).filter(notice.ID == noticeCandidate_.noticeID).first()
                    db.session.delete(noticeCandidate_)
                    db.session.delete(notice__)
                    db.session.delete(target)
                    db.session.commit()
                    if task_.db_task_taskCandidate == []:
                        task_.taskStatus = 0
                        db.session.commit()
                    db.session.commit()
                    notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['cancelAccepting'], haveRead = 0)
                    db.session.add(notice_)
                    db.session.commit()
                    notice_task = noticeTask(noticeID = notice_.ID, taskID = task_.taskID)
                    db.session.add(notice_task)
                    db.session.commit()
                    oldNotice_ = db.session.query(notice).filter(notice.userID == userID_).filter(notice.status == noticeType['haveCandidate']).first()
                    oldNotice_candidate = db.session.query(noticeCandidate).filter(noticeCandidate.noticeID == oldNotice_.ID)
                    db.session.delete(oldNotice_candidate)
                    db.session.delete(oldNotice_)
                    db.session.commit()
                    return jsonify({"rspCode":200})
        except:
            #任務不可取消
            return jsonify({"rspCode":402}) 
    elif task_.SP[0].userID != int(userID_):
        return jsonify({"rspCode":401})   
    elif task_.taskStatus == 2:
        task_.taskStatus =10
        notice_ = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['SPCancel'], haveRead = 0)
        db.session.add(notice_)
        db.session.commit()
        notice_task = noticeTask(noticeID = notice_.ID, taskID = task_.taskID)
        db.session.add(notice_task)
        db.session.commit()
        db.session.commit()
        return jsonify({"rspCode":200})
    elif task_.taskStatus == 9:
        task_.taskStatus = 11
        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['cancelTask'], haveRead = 0)
        db.session.add(notice_)
        db.session.commit()
        notice_task = noticeTask(noticeID = notice_.ID, taskID = task_.taskID)
        db.session.add(notice_task)
        db.session.commit()
        notice_2 = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['cancelTask'], haveRead = 0)
        db.session.add(notice_2)
        db.session.commit()
        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = task_.taskID)
        db.session.add(notice_task_2)
        db.session.commit()
        db.engine.execute(drop_plzComment(taskID_))
        db.engine.execute(drop_taskEndTime_sql(taskID_))
        return jsonify({"rspCode":200})
    #任務不可取消
    return jsonify({"rspCode":402})
#完成或未完成 SP、SR共用
#傳taskID,status
#回傳rspCode
@Task.route("/task_finish_or_not", methods =['POST'])
def task_finish_or_not():
    if request.method != 'POST':
        return jsonify({"rspCode":300})
    try:
        userID_ = int(session.get('userID'))
    except:
        #尚未登入
        return jsonify({"rspCode":500})
    if session.get('userType') != userType['USER']:
        return jsonify({"rspCode":500})
    json = request.get_json()
    taskID_ = json['taskID']
    status = json['status']
    print(json)
    task_ = db.session.query(task).filter(task.taskID == taskID_).first()
    if task_ == None:
        #任務不存在
        return jsonify({"rspCode":400})
    if datetime.datetime.now() > task_.taskEndTime + datetime.timedelta(hours=1) or datetime.datetime.now() < task_.taskStartTime:
        #不在可評價時間
        return jsonify([datetime.datetime.now(),task_.taskEndTime + datetime.timedelta(hours=1)])
        return jsonify({"rspCode":401})
    if not(status in ['0','1']):
        #status 只能是 0 or 1
        return jsonify({"rspCode":403}) 
    if task_.SR[0].userID == int(userID_) :
        if task_.taskStatus in [2,16,15,9,10]:
            if status == '1':
                if task_.taskStatus == 2 or task_.taskStatus == 9 or task_.taskStatus == 10:
                    notice_ = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['SRFinish'], haveRead = 0)
                    db.session.add(notice_)
                    db.session.commit()
                    notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                    db.session.add(notice_task)
                    db.session.commit()
                    task_.taskStatus = 13
                    now_ = datetime.datetime.now()
                elif task_.taskStatus == 16:
                    if datetime.datetime.now() < task_.taskEndTime:
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_)
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 3
                elif task_.taskStatus == 15:
                    if datetime.datetime.now() < task_.taskEndTime:
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_)
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 6
                task_.SR[0].userPoint -= task_.taskPoint
                task_.SP[0].userPoint += task_.taskPoint
                pointList = db.session.query(point).filter(point.ownerID == int(userID_)).limit(task_.taskPoint).all()                
                now_ = datetime.datetime.now()
                for p in pointList:
                    p.ownerID = task_.SP[0].userID
                    p.time = now_
                    pointRecord_ = pointRecord(pointID = p.ID, ownerID = task_.SP[0].userID, transferTime = now_)
                    db.session.add(pointRecord_)
                    db.session.commit()
                db.session.commit()
                if task_.taskPoint != 0:
                    #SR
                    transferRecord_ = transferRecord(userID = task_.SR[0].userID,time = datetime.datetime.now())
                    db.session.add(transferRecord_)
                    db.session.commit()
                    transferRecordTask_ = transferRecordTask(transferRecordID = transferRecord_.transferRecordID, taskID = taskID_)
                    db.session.add(transferRecordTask_)
                    db.session.commit()
                    #SP
                    transferRecord_2 = transferRecord(userID = task_.SP[0].userID,time = datetime.datetime.now())
                    db.session.add(transferRecord_2)
                    db.session.commit()
                    transferRecordTask_2 = transferRecordTask(transferRecordID = transferRecord_2.transferRecordID, taskID = taskID_)
                    db.session.add(transferRecordTask_2)
                    db.session.commit()
                return jsonify({"rspCode":200})
            elif status == '0':
                if task_.taskStatus == 2 or task_.taskStatus == 9 or task_.taskStatus == 10:
                    notice_ = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['SRFinish'], haveRead = 0)
                    db.session.add(notice_)
                    db.session.commit()
                    notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                    db.session.add(notice_task)
                    db.session.commit()
                    task_.taskStatus = 14
                elif task_.taskStatus == 16:
                    if datetime.datetime.now() < task_.taskEndTime:
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_)
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 7
                elif task_.taskStatus == 15:
                    if datetime.datetime.now() < task_.taskEndTime:
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_)
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SP[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 8
                db.session.commit()
                return jsonify({"rspCode":200})
        else:
            #不能這樣做
            return jsonify({"rspCode":402})
    elif task_.SP[0].userID == int(userID_) :
        if task_.taskStatus in [2,14,13,9,10]:
            if status == '1':
                if task_.taskStatus == 2 or task_.taskStatus == 9 or task_.taskStatus == 10:
                    notice_ = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['SPFinish'], haveRead = 0)
                    db.session.add(notice_)
                    db.session.commit()
                    notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                    db.session.add(notice_task)
                    db.session.commit()
                    task_.taskStatus = 16
                elif task_.taskStatus == 13:
                    if str(datetime.datetime.now()) < str(task_.taskEndTime):
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_) 
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 3
                elif task_.taskStatus == 14:
                    if str(datetime.datetime.now()) < str(task_.taskEndTime):
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_)
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 7
                db.session.commit()
                return jsonify({"rspCode":200})
            elif status == '0':
                if task_.taskStatus == 2 or task_.taskStatus == 9 or task_.taskStatus == 10:
                    notice_ = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['SPFinish'], haveRead = 0)
                    db.session.add(notice_)
                    db.session.commit()
                    notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                    db.session.add(notice_task)
                    db.session.commit()
                    task_.taskStatus = 8
                elif task_.taskStatus == 13:
                    if str(datetime.datetime.now()) < str(task_.taskEndTime):
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_)
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 6
                elif task_.taskStatus == 14:
                    if str(datetime.datetime.now()) < str(task_.taskEndTime):
                        notice_ = notice(userID = userID_,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_)
                        db.session.commit()
                        notice_task = noticeTask(noticeID = notice_.ID, taskID = int(taskID_))
                        db.session.add(notice_task)
                        db.session.commit()
                        notice_2 = notice(userID = task_.SR[0].userID,time = datetime.datetime.now(), status = noticeType['taskFinish'], haveRead = 0)
                        db.session.add(notice_2)
                        db.session.commit()
                        notice_task_2 = noticeTask(noticeID = notice_2.ID, taskID = int(taskID_))
                        db.session.add(notice_task_2)
                        db.session.commit()
                    task_.taskStatus = 8
                db.session.commit()
                return jsonify({"rspCode":200})
        else:
            #不能這樣做
            return jsonify({"rspCode":402})
    else:
        #不是SP或SR
        return jsonify({"rspCode":404})
