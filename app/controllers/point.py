from flask import Blueprint, request, session, jsonify
from ..models.model import *
from ..models import userType

Point = Blueprint('point', __name__)

#取得點數數量
@Point.route('/total', methods=['GET'])
def total():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            try:
                query_data = account.query.filter_by(userID = userID).first()
                if query_data == None:
                    return jsonify({"rspCode": "401", "point": ""})                     #ID錯誤
            except:
                return jsonify({"rspCode": "400", "point": ""})                         #資料庫錯誤
            return jsonify({"rspCode": "200", "point": query_data.userPoint})              #成功取得
        else:
            return jsonify({"rspCode": "500", "point": ""})                             #權限不符
    else:
        return jsonify({"rspCode": "300", "point": ""})                                 #method

#取得點數紀錄數量
@Point.route('/record_amount', methods=['POST'])
def record_amount():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": "40"})                                           #非法字元
        userID = value['userID']
        try:
            query_data = transferRecord.query.filter_by(userID = userID).order_by(transferRecord.time).all()
        except:
            return jsonify({"rspCode": "30"})                                           #伺服器錯誤
        pointRecordIDList = []  
        for transferRecord_ in query_data:
            pointRecordIDList.append(transferRecord_.transferRecordID)
        return jsonify({"rspCode": "20", "pointRecordIDList": pointRecordIDList})

#取得點數紀錄
@Point.route('/record', methods=['POST'])
def record():
    if request.method == 'POST':
        try:
            value = request.get_json()
        except:
            return jsonify({"rspCode": "40"})                                           #非法字元
        userID = value['userID']
        recordStartID = value['recordID']
        requestAmount = value ['requestAmount']
        try:
            query_data = transferRecord.query.filter_by(userID = userID).order_by(transferRecord.time).all()
        except:
            return jsonify({"rspCode": "30"})                                           #伺服器錯誤
        print(query_data)
        pointRecord = []
        count = 0
        start = False
        for record in query_data:
            if record.transferRecordID == recordStartID:
                start = True
            if start:
                count = count + 1
                if record.db_transferRecord_transferRecordAllotment:
                    if record.db_transferRecord_transferRecordAllotment[0].allotment.period == 0:
                        pointRecord.append({"subject": 1, "detail": "一次性",\
                                        "amount": record.db_transferRecord_transferRecordAllotment[0].allotment.quota, "time": str(record.time)})
                    else:
                        pointRecord.append({"subject": 1, "detail": "{}/{}".format(record.db_transferRecord_transferRecordAllotment[0].times,\
                                            record.db_transferRecord_transferRecordAllotment[0].allotment.frequency),\
                                            "amount": record.db_transferRecord_transferRecordAllotment[0].allotment.quota, "time": str(record.time)})
                elif record.db_transferRecord_transferRecordApply:
                    if record.db_transferRecord_transferRecordApply[0].apply.applyCondition.period == 0:
                        pointRecord.append({"subject": 2, "detail": "一次性",\
                                            "amount": record.db_transferRecord_transferRecordApply[0].apply.applyCondition.quota,\
                                            "time": str(record.time)})
                    else:
                        pointRecord.append({"subject": 2, "detail": "{}/{}".format(record.db_transferRecord_transferRecordApply[0].times,\
                                            record.db_transferRecord_transferRecordApply[0].apply.frequency),\
                                            "amount": record.db_transferRecord_transferRecordApply[0].apply.applyCondition.quota,\
                                            "time": str(record.time)})
                elif record.db_transferRecord_transferRecordTask:
                    if record.db_transferRecord_transferRecordTask[0].task.SR[0].userID == userID:
                        pointRecord.append({"subject": 3, "detail": record.db_transferRecord_transferRecordTask[0].task.taskName,
                                            "amount": -1 * record.db_transferRecord_transferRecordTask[0].task.taskPoint, "time": str(record.time)})
                    else:
                        pointRecord.append({"subject": 3, "detail": record.db_transferRecord_transferRecordTask[0].task.taskName,
                                            "amount": record.db_transferRecord_transferRecordTask[0].task.taskPoint, "time": str(record.time)})
            if count == requestAmount:
                break
        print(pointRecord)
        return jsonify({"rspCode": "20", "pointRecord": pointRecord})