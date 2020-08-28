from flask import Blueprint, session, jsonify, request
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
            print(value)
            userID = value['userID']
            try:
                query_data = account.query.filter_by(userID = userID).first()
            except:
                return jsonify({"rspCode": "400", "userID": "", "name": "", "userGender": "", "userAge": "", "userInfo": ""})       #資料庫錯誤
            other_day = query_data.userBirthday
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
            print(value, 123)
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

#取得個人頁面雇員評分數量
@Profile.route('/SP_rate_amount', methods=['POST'])
def SP_rate_amount():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": "41"})                                                                          #非法文字
            userID = value['userID']
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data == None:
                    return jsonify({"rspCode": "42"})                                                                      #該userID不存在
            except:
                return jsonify({"rspCode": "30"})                                                                          #資料庫錯誤
            commentList = []
            print(query_data.taskSP)
            for task in query_data.taskSP:
                if task.taskStatus != 11 and task.taskStatus != 12:
                    if task.db_task_comment[0].commentStatus == 1:
                        if task.db_task_comment[0].SRComment:
                            commentList.append(task.db_task_comment[0])
            return jsonify({"rspCode": "20", "rateAmount": len(commentList)})                                            #取得成功
        else:
            return jsonify({"rspCode": "50"})                                                                            #權限不符
    else:
        return jsonify({"rspCode": "31"})                                                                                #method使用錯誤
        


#取得個人頁面雇員
@Profile.route('/SP_rate', methods=['POST'])
def SP_rate():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": "41"})                                                                          #非法文字
            userID = value['userID']
            try:
                query_data = account.query.filter_by(userID = userID).first()
            except:
                return jsonify({"rspCode": "30"})                                                                          #資料庫錯誤
            startNum = value['startNum']
            amount = value['amount']
            commentList = []
            for task in query_data.taskSP:
                if task.taskStatus != 11 and task.taskStatus != 12:
                    if task.db_task_comment[0].commentStatus == 1:
                        if task.db_task_comment[0].SRComment:
                            commentList.append(task.db_task_comment[0])
            rateListJson = []
            for i in range(startNum, startNum + amount):
                rateListJson.append({"commentBy": commentList[i].task.SR[0].name, "rate": int(commentList[i].SRComment[0]),\
                                            "comment": commentList[i].SRComment[2:]})
            print(rateListJson)
            return jsonify({"rspCode": "20", "rateList": rateListJson})                                                    #取得成功
        else:
            return jsonify({"rspCode": "50"})                                                                              #權限不符
    else:
        return jsonify({"rspCode": "31"})                                                                              #method使用錯誤

#取得個人頁面雇主評分數量
@Profile.route('/SR_rate_amount', methods=['POST'])
def SR_rate_amount():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": "41"})                                                                          #非法文字
            print(value)
            userID = value['userID']
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data == None:
                    return jsonify({"rspCode": "42"})                                                                      #該userID不存在
            except:
                return jsonify({"rspCode": "30"})                                                                          #資料庫錯誤
            commentList = []
            print(query_data.taskSR)
            for task in query_data.taskSR:
                if task.taskStatus != 11 and task.taskStatus != 12:
                    if task.db_task_comment[0].commentStatus == 1:
                        if task.db_task_comment[0].SPComment:
                            commentList.append(task.db_task_comment[0])
            print(commentList)
            return jsonify({"rspCode": "20", "rateAmount": len(commentList)})                                            #取得成功
        else:
            return jsonify({"rspCode": "50"})                                                                              #權限不符
    else:
        return jsonify({"rspCode": "31"})                                                                              #method使用錯誤

#取得個人頁面雇主
@Profile.route('/SR_rate', methods=['POST'])
def SR_rate():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": "41"})                                                                          #非法文字
            userID = value['userID']
            try:
                query_data = account.query.filter_by(userID = userID).first()
            except:
                return jsonify({"rspCode": "30"})                                                                          #資料庫錯誤
            startNum = value['startNum']
            amount = value['amount']
            commentList = []
            for task in query_data.taskSR:
                if task.taskStatus != 11 and task.taskStatus != 12:
                    if task.db_task_comment[0].commentStatus == 1:
                        if task.db_task_comment[0].SPComment:
                            commentList.append(task.db_task_comment[0])
            rateListJson = []
            for i in range(startNum, startNum + amount):
                print(i)
                rateListJson.append({"commentBy": commentList[i].task.SP[0].name, "rate": int(commentList[i].SPComment[0]),\
                                            "comment": commentList[i].SPComment[2:]})
            print(rateListJson)
            return jsonify({"rspCode": "20", "rateList": rateListJson})                                                    #取得成功
        else:
            return jsonify({"rspCode": "50"})                                                                              #權限不符
    else:
        return jsonify({"rspCode": "31"})                                                                              #method使用錯誤