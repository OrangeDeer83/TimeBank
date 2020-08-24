from flask import Blueprint, render_template, session, jsonify, request
from ..models.model import *
from ..models import userType
from math import floor

Profile = Blueprint('profile', __name__)

#取得個人資料
@Profile.route('/output/info', methods=['POST'])
def output_info():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": "401", "userID": "", "name": "", "userGender": "", "userAge": "", "userInfo": ""})       #非法字元
            userID = value['userID']
            try:
                query_data = account.query.filter_by(userID = userID).first()
            except:
                return jsonify({"rspCode": "400", "userID": "", "name": "", "userGender": "", "userAge": "", "userInfo": ""})       #資料庫錯誤
            other_day = transferToDate(query_data.userBirthday)
            userAge = floor((datetime.date.today() - other_day).days/365.25)
            return jsonify({"rspCode": "200", "userID": userID, "name": query_data.name, "userGender": query_data.userGender,\
                            "userAge": userAge, "userInfo": query_data.userInfo})                                                   #成功取得個人資料
        else:
            return jsonify({"rspCode": "500", "userID": "", "name": "", "userGender": "", "userAge": "", "userInfo": ""})           #權限不符
    else:
        return jsonify({"rspCode": "300", "userID": "", "name": "", "userGender": "", "userAge": "", "userInfo": ""})               #method使用錯誤

#取得個人頁面已發任務
@Profile.route('/output/task', methods=['POST'])
def output_task():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": "402", "taskWaiting": ""})       #非法字元
            userID = value['userID']
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data == None:
                    return jsonify({"rspCode": "401", "taskWaiting": ""})                                              #userID錯誤
            except:
                return jsonify({"rspCode": "400", "taskWaiting": ""})                                                  #資料庫錯誤
            taskWaiting = []
            for task in query_data.taskSR:
                if task.taskStatus in [0, 1]:
                    taskWaiting.append(task)
            sortTaskByTaskID(taskWaiting, 0, len(taskWaiting) - 1)
            taskWaitingJson = []
            for task in taskWaiting:
                taskWaitingJson.append({"taskID": task.taskID, "taskName": task.taskName, "taskPoint": task.taskPoint,\
                                        "taskStartTime": str(task.taskStartTime), "taskEndTime": str(task.taskEndTime)})
            return jsonify({"rspCode": "200", "taskWaiting": taskWaitingJson})                                        #成功取得
        else:
            return jsonify({"rspCode": "500", "taskWaiting": ""})                                                     #權限不符 
    else:
        return jsonify({"rspCode": "300", "taskWaiting": ""})                                                         #method使用錯誤

#取得個人頁面雇員
@Profile.route('/', methods=['POST'])
def SP():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": "401"})                                                                          #非法文字
        userID = value['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
        except:
            return jsonify({"rspCode": "400"})                                                                          #資料庫錯誤
        
        for task in query_data:
            pass


#取得個人頁面雇主
@Profile.route('/', methods=['POST'])
def SR():
    pass