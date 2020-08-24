from flask import Blueprint, jsonify, request, session
from ..models.model import *
import datetime

Calender = Blueprint('calender', __name__)

days_of_month = {1: 31, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31,\
                8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

#取得當月行事曆
@Calender.route('/one_month_list', methods=['POST'])
def one_month_list():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": "40"})                                                                          #非法文字
        show_year = value['year']
        show_month = value['month']
        userID = value['userID']
        if show_month < 1 or show_month > 12:
            return jsonify({"rspCode": "41"})                                                                          #月份錯誤
        try:
            query_data = account.query.filter_by(userID = userID).first()
            if query_data == None:
                return jsonify({"rspCode": "42"})                                                                      #沒有該user
        except:
            return jsonify({"rspCode": "30"})                                                                          #資料庫錯誤
        if show_month != 2:
            days = days_of_month[show_month]
        else:
            if show_year % 4 == 0:
                if show_year % 100 == 0:
                    days = 29
                else:
                    days = 28
            else:
                days = 28
        dateList = []
        for day in range(1, days + 1):
            dateStart = datetime.datetime(show_year, show_month, day, 0, 0, 0)
            dateEnd = datetime.datetime(show_year, show_month, day, 23, 59, 59)
            Found = False
            for task in query_data.taskSR:
                #確定不是取消跟刪除
                if  task.taskStatus != 4 and task.taskStatus != 11 and task.taskStatus != 12:
                    if dateStart > task.taskStartTime and dateStart < task.taskEndTime:
                        dateList.append(1)
                        Found = True
                        break
                    elif dateEnd > task.taskStartTime and dateEnd < task.taskEndTime:
                        dateList.append(1)
                        Found = True
                        break
                    elif dateStart < task.taskStartTime and dateEnd > task.taskStartTime:
                        dateList.append(1)
                        Found = True
                        break
                    elif dateStart < task.taskStartTime and dateEnd > task.taskEndTime:
                        dateList.append(1)
                        Found = True
                        break
            if not Found:
                for taskCandidate_ in query_data.db_account_taskCandidate:
                    #還在申請中
                    if taskCandidate_.task.taskStatus == 1:
                        if dateStart > taskCandidate_.task.taskStartTime and dateStart < taskCandidate_.task.taskEndTime:
                            dateList.append(1)
                            Found = True
                            break
                        elif dateEnd > taskCandidate_.task.taskStartTime and dateEnd < taskCandidate_.task.taskEndTime:
                            dateList.append(1)
                            Found = True
                            break
                        elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskStartTime:
                            dateList.append(1)
                            Found = True
                            break
                        elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskEndTime:
                            dateList.append(1)
                            Found = True
                            break
                    #已經接到或是完成
                    elif taskCandidate_.task.taskStatus > 1 and taskCandidate_.task.taskStatus != 4 and taskCandidate_.task.taskStatus != 11 and taskCandidate_.task.taskStatus != 12:
                        #確定SP是自己
                        if taskCandidate_.task.SP[0].userID == userID:
                            if dateStart > taskCandidate_.task.taskStartTime and dateStart < taskCandidate_.task.taskEndTime:
                                dateList.append(1)
                                Found = True
                                break
                            elif dateEnd > taskCandidate_.task.taskStartTime and dateEnd < taskCandidate_.task.taskEndTime:
                                dateList.append(1)
                                Found = True
                                break
                            elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskStartTime:
                                dateList.append(1)
                                Found = True
                                break
                            elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskEndTime:
                                dateList.append(1)
                                Found = True
                                break
            if not Found:
                dateList.append(0)
        print(dateList)
        return jsonify({"rspCode": "20", "dateList": dateList})                                                                         #成功取得
    else:
        return jsonify({"rspCode": "31"})                                                                                                 #method使用錯誤

#取得當日行事曆
@Calender.route('/one_date_list', methods=['POST'])
def one_date_list():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": "40"})                                                                          #非法文字
        show_year = value['year']
        show_month = value['month']
        show_day = value['day']
        userID = value['userID']
        try:
            query_data = account.query.filter_by(userID = userID).first()
            if query_data == None:
                return jsonify({"rspCode": "41"})                                                                      #沒有該user
        except:
            return jsonify({"rspCode": "30"})                                                                          #資料庫錯誤
        taskList = []
        dateStart = datetime.datetime(show_year, show_month, show_day, 0, 0, 0)
        dateEnd = datetime.datetime(show_year, show_month, show_day, 23, 59, 59)
        for task in query_data.taskSR:
            if  task.taskStatus != 4 and task.taskStatus != 11 and task.taskStatus != 12:
                if dateStart > task.taskStartTime and dateStart < task.taskEndTime:
                    taskList.append(task)
                elif dateEnd > task.taskStartTime and dateEnd < task.taskEndTime:
                    taskList.append(task)
                elif dateStart < task.taskStartTime and dateEnd > task.taskStartTime:
                    taskList.append(task)
                elif dateStart < task.taskStartTime and dateEnd > task.taskEndTime:
                    taskList.append(task)
        for taskCandidate_ in query_data.db_account_taskCandidate:
            #還在申請中
            if taskCandidate_.task.taskStatus == 1:
                if dateStart > taskCandidate_.task.taskStartTime and dateStart < taskCandidate_.task.taskEndTime:
                    taskList.append(taskCandidate_.task)
                elif dateEnd > taskCandidate_.task.taskStartTime and dateEnd < taskCandidate_.task.taskEndTime:
                    taskList.append(taskCandidate_.task)
                elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskStartTime:
                    taskList.append(taskCandidate_.task)
                elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskEndTime:
                    taskList.append(taskCandidate_.task)
            #已經接到或是完成
            elif taskCandidate_.task.taskStatus > 1 and taskCandidate_.task.taskStatus != 4 and taskCandidate_.task.taskStatus != 11 and taskCandidate_.task.taskStatus != 12:
                 #確定SP是自己
                if taskCandidate_.task.SP[0].userID == userID:
                    if dateStart > taskCandidate_.task.taskStartTime and dateStart < taskCandidate_.task.taskEndTime:
                        taskList.append(taskCandidate_.task)
                    elif dateEnd > taskCandidate_.task.taskStartTime and dateEnd < taskCandidate_.task.taskEndTime:
                        taskList.append(taskCandidate_.task)
                    elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskStartTime:
                        taskList.append(taskCandidate_.task)
                    elif dateStart < taskCandidate_.task.taskStartTime and dateEnd > taskCandidate_.task.taskEndTime:
                        taskList.append(taskCandidate_.task)
        sortTaskByTaskStartTime(taskList, 0, len(taskList) - 1)
        print(taskList)
        taskListJson = []
        for task in taskList:
            if task.taskStatus == 0:
                taskListJson.append({"taskName": task.taskName, "taskStartTime": task.taskStartTime,\
                                    "taskEndTime": task.taskEndTime, "taskContent": task.taskContent, "taskLocation": task.taskLocation,\
                                    "taskSRName": "", "taskSPName": ""})
            elif task.taskStatus == 1:
                taskListJson.append({"taskName": task.taskName + "(申請中)", "taskStartTime": task.taskStartTime,\
                                    "taskEndTime": task.taskEndTime, "taskContent": task.taskContent, "taskLocation": task.taskLocation,\
                                    "taskSRName": task.SR[0].userName, "taskSPName": ""})
            elif task.taskStatus > 1 and task.taskStatus != 4 and task.taskStatus != 11 and task.taskStatus != 12:
                if task.SP[0].userID == userID:
                    taskListJson.append({"taskName": task.taskName, "taskStartTime": task.taskStartTime,\
                                    "taskEndTime": task.taskEndTime, "taskContent": task.taskContent, "taskLocation": task.taskLocation,\
                                    "taskSRName": "", "taskSPName": task.SP[0].userName})
                elif task.SR[0].userID == userID:
                    taskListJson.append({"taskName": task.taskName, "taskStartTime": task.taskStartTime,\
                                    "taskEndTime": task.taskEndTime, "taskContent": task.taskContent, "taskLocation": task.taskLocation,\
                                    "taskSRName": task.SR[0].userName, "taskSPName": ""})
        return jsonify({"rspCode": "20", "taskList": taskListJson})                                                 #成功取得
    else:
        return jsonify({"rspCode": "31"})                                                                           #method使用錯誤