from flask import Blueprint, session, jsonify, request
from ..models.model import *
from ..models import db, userType

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
                        return jsonify({"rspCode": "401", "taskRecord": ""})                                   #沒有該帳號                                     #userID錯誤
                except:
                    return jsonify({"rspCode": "400", "taskRecord": ""})                                       #資料庫錯誤
                taskRecord = []
                for task in query_data.taskSR:
                    if task.taskStatus in [4, 5, 12, 15]:
                        taskRecord.append(task)
                sortTask(taskRecord, 0, len(taskRecord) - 1)
                taskRecordJson = []
                for task in taskRecord:
                    if len(task.SP) == 0:
                        SPname = ""
                    else:
                        SPname = task.SP[0].name
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
                    taskRecordJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSP": SPname, "taskSR": task.SR[0].name,\
                                            "SPComment": SPComment, "SPScore": SPScore, "SRComment": SRComment, "SRScore": SRScore})
                return jsonify({"rspCode": "200", "taskRecord": taskRecordJson})                    #成功取得
            else:
                return jsonify({"rspCode": "402", "taskRecord": ""})                                #沒有userID
        else:
            return jsonify({"rspCode": "500", "taskRecord": ""})                                    #權限不符
    else:
        return jsonify({"rspCode": "300", "taskRecord": ""})                                        #method使用錯誤

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
                        return jsonify({"rspCode": "401", "taskPassed": ""})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": "400", "taskPassed": ""})                                                  #資料庫錯誤
                taskPassed = []
                for task in query_data.taskSP:
                    if task.taskStatus in [2, 3, 6, 7, 8, 9, 10, 13, 14]:
                        taskPassed.append(task)
                sortTask(taskPassed, 0, len(taskPassed) - 1)
                taskPassedJson = []
                for task in taskPassed:
                    taskPassedJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name})
                return jsonify({"rspCode": "200", "taskPassed": taskPassedJson})                                        #成功取得
            else:
                return jsonify({"rspCode": "402", "taskRecord": ""})                                #沒有userID
        else:
            return jsonify({"rspCode": "500", "taskRecord": ""})                                    #權限不符
    else:
        return jsonify({"rspCode": "300", "taskPassed": ""})                                                    #method使用錯誤

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
                        return jsonify({"rspCode": "401", "taskChecking": ""})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": "400", "taskChecking": ""})                                                  #資料庫錯誤
                taskChecking = []
                for candidate in query_data:
                    print(candidate.task.taskStatus)
                    if candidate.task.taskStatus == 1:
                        taskChecking.append(candidate.task)
                sortTask(taskChecking, 0, len(taskChecking) - 1)
                taskCheckingJson = []
                for task in taskChecking:
                    taskCheckingJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSR": task.SR[0].name})
                return jsonify({"rspCode": "200", "taskChecking": taskCheckingJson})                                        #成功取得
            else:
                return jsonify({"rspCode": "402", "taskRecord": ""})                                #沒有userID
        else:
            return jsonify({"rspCode": "500", "taskRecord": ""})                                    #權限不符
    else:
        return jsonify({"rspCode": "300", "taskChecking": ""})                                                      #method使用錯誤

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
                        return jsonify({"rspCode": "401", "taskRefused": ""})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": "400", "taskRefused": ""})                                                  #資料庫錯誤
                taskRefused = []
                for candidate in query_data:
                    if candidate.task.taskStatus >= 2 and candidate.task.SP[0].userID != userID:
                        taskRefused.append(candidate.task)
                sortTask(taskRefused, 0, len(taskRefused) - 1)
                taskRefusedJson = []
                for task in taskRefused:
                    taskRefusedJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSP": task.SP[0].name, "taskSR": task.SR[0].name})
                return jsonify({"rspCode": "200", "taskRefused": taskRefusedJson})                                        #成功取得
            else:
                return jsonify({"rspCode": "402", "taskRecord": ""})                                #沒有userID
        else:
            return jsonify({"rspCode": "500", "taskRecord": ""})                                    #權限不符
    else:
        return jsonify({"rspCode": "300", "taskRefused": ""})                                                     #method使用錯誤

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
                        return jsonify({"rspCode": "401", "taskRecord": ""})                                              #userID錯誤
                except:
                    return jsonify({"rspCode": "400", "taskRecord": ""})                                                  #資料庫錯誤
                taskRecord = []
                for task in query_data.taskSP:
                    if task.taskStatus  not in [5, 11, 15]:
                        taskRecord.append(task)
                sortTask(taskRecord, 0, len(taskRecord) - 1)
                taskRecordJson = []
                for task in taskRecord:
                    if len(task.SP) == 0:
                        SPname = ""
                    else:
                        SPname = task.SP[0].name
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
                    taskRecordJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskContent": task.taskContent,\
                                            "taskPoint": task.taskPoint, "taskLocation": task.taskLocation,\
                                            "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime),\
                                            "taskStatus": task.taskStatus, "taskSP": SPname, "taskSR": task.SR[0].name,\
                                            "SPComment": SPComment, "SPScore": SPScore, "SRComment": SRComment, "SRScore": SRScore})
                return jsonify({"rspCode": "200", "taskRecord": taskRecordJson})                                        #成功取得
            else:
                return jsonify({"rspCode": "402", "taskRecord": ""})                                #沒有userID
        else:
            return jsonify({"rspCode": "500", "taskRecord": ""})                                    #權限不符
    else:
        return jsonify({"rspCode": "300", "taskRecord": ""})                                                     #method使用錯誤
