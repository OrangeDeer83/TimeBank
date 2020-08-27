from flask import Blueprint, session, jsonify, request
from ..models.model import *
from ..models import db, userType, noticeType, noticePage

Notice = Blueprint('notice', __name__)

#取得有無新通知
@Notice.route('/new_indicate', methods=['GET'])
def new_indicate():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            try:
                query_data = notice.query.filter_by(userID = userID, haveRead = 0).first()
            except:
                return jsonify({"rspCode": "30"})                           #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": "20", "notice": 0})              #沒有新通知
            else:
                return jsonify({"rspCode": "20", "notice": 1})              #有新通知
        else:
            return jsonify({"rspCode": "50"})                               #權限不符
    else:
        return jsonify({"rspCode": "31"})                                   #method使用錯誤

#取得新通知
@Notice.route('/new_list', methods=['GET'])
def new_list():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            try:
                query_data = notice.query.filter_by(userID = userID, haveRead = 0).first()
            except:
                return jsonify({"rspCode": "30"})                                   #資料庫錯誤
            if query_data == None:
                return jsonify({"rspCode": "20", "newNoticeList": ""})              #沒有新通知
            newNoticeList = []
            for notice_ in query_data:
                if notice_.db_notice_noticeTask:
                    if notice_.status == noticeType['taskWillStart']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 11:
                            db.session.delete(notice)
                            db.session.commit()
                        #該USER為雇員
                        elif notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            newNoticeList.append({"content": "「{}」任務將在一小時後開始。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            newNoticeList.append({"content": "「{}」任務將在一小時後開始。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                    elif notice_.status == noticeType['taskStart']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 11:
                            db.session.delete(notice)
                            db.session.commit()
                        #該USER為雇員
                        elif notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            newNoticeList.append({"content": "「{}」任務開始，完成後請至雇員已通過頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            newNoticeList.append({"content": "「{}」任務開始，完成後請至雇主已接受頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                    elif notice_.status == noticeType['NoSP']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 12 or notice_.db_notice_noticeTask[0].task.SP == None:
                            db.session.delete(notice)
                            db.session.commit()
                        else:
                            newNoticeList.append({"content": "「{}」任務時間已到，仍無人承接，，可至歷史紀錄查看任務細節。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['taskEndTime']:
                        finished = False
                        for noticeTask_ in notice_.db_notice_noticeTask[0].task.db_task_noticeTask:
                            if noticeTask_.notice_.status == noticeType['taskFinish']:
                                finished = True
                                db.session.delete(notice)
                                db.session.commit()
                                break
                        if not Finished:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                newNoticeList.append({"content": "「{}」任務已結束。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                newNoticeList.append({"content": "「{}」任務已結束。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['createTask']:
                        newNoticeList.append({"content": "已成功功建立任務「{}」。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['cancelAccepting']:
                        newNoticeList.append({"content": "已收回您「{}」的任務申請。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SPPassed']:
                        newNoticeList.append({"content": "{}已接受您「{}」的任務申請，請至所有任務雇員已通過頁面查看。".format(\
                            notice_.db_notice_noticeTask[0].task.SR.name,\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SRCancel']:
                        newNoticeList.append({"content": "{}取消任務「{}」，若同意取消請至所有任務雇主已接受頁面點選取消，若不同意請忽略此訊息。".format(\
                            notice_.db_notice_noticeTask[0].task.SR.name,\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                    elif notice_.status == noticeType['SPCancel']:
                        newNoticeList.append({"content": "{}取消任務「{}」，若同意取消請至所有任務雇員已通過頁面點選取消，若不同意請忽略此則訊息".format(\
                            notice_.db_notice_noticeTask[0].task.SP.name,\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['cancelTask']:
                        #該USER為雇員
                        if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            newNoticeList.append({"content": "{}已同意取消任務「{}」，可至歷史紀錄查看任務細節。".format(\
                                notice_.db_notice_noticeTask[0].task.SR.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            newNoticeList.append({"content": "{}已同意取消任務「{}」，可至歷史紀錄查看任務細節。".format(\
                                notice_.db_notice_noticeTask[0].task.SP.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['deleteTask']:
                        newNoticeList.append({"content": "已成功刪除任務「{}」。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['editTask']:
                        newNoticeList.append({"content": "已成功編輯任務「{}」。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SRFinish']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 13:
                            newNoticeList.append({"content": "「{}」{}已點選完成，請至雇員已通過頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SR.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        elif notice_.db_noticeTask[0].task.taskStatus == 14:
                            newNoticeList.append({"content": "「{}」{}已點選未完成，請至雇員已通過頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SR.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SPFinish']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 13:
                            newNoticeList.append({"content": "「{}」{}已點選完成，請至雇主已接受頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SP.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        elif notice_.db_noticeTask[0].task.taskStatus == 14:
                            newNoticeList.append({"content": "「{}」{}已點選未完成，請至雇主已接受頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SP.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['taskFinish']:
                        #該USER為雇員
                        if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            newNoticeList.append({"content": "「{}」任務已結束。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            newNoticeList.append({"content": "「{}」任務已結束。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['pleaseComment']:
                        #還在評論狀態
                        if notice_.db_notice_noticeTask[0].task.db_task_comment[0].commentStatus == -1:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                if notice_.db_notice_noticeTask[0].task.db_task_comment[0].SPComment:
                                    newNoticeList.append({"content": "您尚未對「{}」評論，請至雇員已通過頁面評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                                else:
                                    db.session.delete(notice)
                                    db.session.commit()
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                if notice_.db_notice_noticeTask[0].task.db_task_comment[0].SRComment:
                                    newNoticeList.append({"content": "您尚未對「{}」評論，請至雇主已接受頁面評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                                else:
                                    db.session.delete(notice)
                                    db.session.commit()
                        #進入審核狀態
                        else:
                            db.session.delete(notice)
                            db.session.commit()
                    elif notice_.status == noticeType['judgeComment']:
                        #評論通過
                        if notice_.db_notice_noticeTask[0].task.db_task_comment[0].commentStatus == 1:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                newNoticeList.append({"content": "管理員已通過您對「{}」的評論，可至歷史紀錄查看。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                newNoticeList.append({"content": "管理員已通過您對「{}」的評論，可至歷史紀錄查看。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                        #評論否決
                        elif notice_.db_notice_noticeTask[0].task.db_task_comment[0].commentStatus == 2:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                newNoticeList.append({"content": "管理員否決了您對「{}」的評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                newNoticeList.append({"content": "管理員否決了您對「{}」的評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                elif notice_.db_notice_noticeCandidate:
                    newNoticeList.append({"content": "{}申請您的任務「{}」，請至所有任務雇主已發布頁面查看。".format(\
                                notice_.db_notice_noticeCandidate[0].taskCandidate.account.name,\
                                notice_.db_notice_noticeCandidate[0].taskCandidate.task.taskName),\
                                "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                elif notice_.db_notice_noticeReport:
                    if notice_.status == noticeType['sendReport']:
                        #該USER為雇員
                        if notice_.db_notice_noticeReport[0].report.task.SP.userID == userID:
                            newNoticeList.append({"content": "「{}」任務的檢舉已送出，管理員正在為您處理。".format(\
                                notice_.db_notice_noticeReport[0].report.task.taskName),\
                                "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeReport[0].report.task.SR.userID == userID:
                            newNoticeList.append({"content": "「{}」任務的檢舉已送出，管理員正在為您處理。".format(\
                                notice_.db_notice_noticeReport[0].report.task.taskName),\
                                "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['judgeReport']:
                        #檢舉通過
                        if notice_.db_notice_noticeReport[0].report.reportStatus == 1:
                            #該USER為雇員
                            if notice_.db_notice_noticeReport[0].report.task.SP.userID == userID:
                                newNoticeList.append({"content": "「{}」任務的檢舉已通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeReport[0].report.task.SR.userID == userID:
                                newNoticeList.append({"content": "「{}」任務的檢舉已通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                        #檢舉未通過
                        elif notice_.db_notice_noticeReport[0].report.reportStatus == 2:
                            #該USER為雇員
                            if notice_.db_notice_noticeReport[0].report.task.SP.userID == userID:
                                newNoticeList.append({"content": "「{}」任務的檢舉未通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeReport[0].report.task.SR.userID == userID:
                                newNoticeList.append({"content": "「{}」任務的檢舉未通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['judgeApply']:
                        #通過
                        if notice_.db_notice_noticeApply[0].apply.applyStatus == 1:
                            if notice_.db_notice_noticeApply[0].apply.result:
                                newNoticeList.append({"content": "點數申請{}：{}通過。".format(\
                                        notice_.noticeApply[0].apply.applyCondition.className,\
                                        notice_.noticeApply[0].apply.result),\
                                        "connectTo": noticePage['pointRecord'], "time": notice_.time})
                            else:
                                newNoticeList.append({"content": "點數申請{}通過。".format(\
                                        notice_.noticeApply[0].apply.applyCondition.className),\
                                        "connectTo": noticePage['pointRecord'], "time": notice_.time})
                        #未通過
                        elif notice_.db_notice_noticeApply[0].apply.applyStatus == 2:
                            #有原因
                            if notice_.db_notice_noticeApply[0].apply.result:
                                newNoticeList.append({"content": "點數申請{}：{}未通過。".format(\
                                    notice_.noticeApply[0].apply.applyCondition.className,\
                                    notice_.noticeApply[0].apply.result),\
                                    "connectTo": noticePage['pointRecord'], "time": notice_.time})
                            #沒有原因
                            else:
                                newNoticeList.append({"content": "點數申請{}未通過。".format(\
                                    notice_.noticeApply[0].apply.applyCondition.className),\
                                    "connectTo": noticePage['pointRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['allotment']:
                        if notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.period == 0:
                            newNoticeList.append({"content": "管理員一次性配發了{}點給您。".format(\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.quota),\
                                "connectTo": noticePage['pointRecord'], "time": notice_.time})
                        else:
                            newNoticeList.append({"content": "管理員配發了{}點給您，{}/{}。".format(\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.quota,\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.times,\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.frequency),\
                                "connectTo": noticePage['pointRecord'], "time": notice_.time})
                notice_.haveRead = 1
                db.session.commit()
            return jsonify({"rspCode": "20", "newNoticeList": newNoticeList})       #成功取得新通知
        else:
            return jsonify({"rspCode": "50"})                                       #權限不符
    else:
        return jsonify({"rspCode": "31"})                                           #method使用錯誤

#取得所有通知的數量
@Notice.route('/all_list_amount', methods=['GET'])
def all_list_amount():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session.get('userID')
            try:
                query_data = notice.query.filter_by(userID = userID).first()
            except:
                return jsonify({"rspCode": "30"})                                   #資料庫錯誤
            return jsonify({"rspCode": "20", "allNoticeAmount": len(query_data)})   #成功取的數量
        else:
            return jsonify({"rspCode": "50"})                                       #權限不符
    else:
        return jsonify({"rspCode": "31"})                                           #method使用錯誤

#取得所有通知
@Notice.route('/all_list', methods=['POST'])
def all_list():
    if request.method == 'POST':
        if session.get('userType') == userType['USER']:
            try:
                value = request.get_json()
            except:
                return jsonify({"rspCode": "40"})                                   #非法文字
            userID = session.get('userID')
            try:
                query_data = notice.query.filter_by(userID = userID).first()
            except:
                return jsonify({"rspCode": "30"})                                   #資料庫錯誤
            startNum = value['startNum']
            amount = value['amount']
            noticeList = []
            for i in (startNum, startNum + amount):
                notice_ = query_data[i]
                if notice_.db_notice_noticeTask:
                    if notice_.status == noticeType['taskWillStart']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 11:
                            db.session.delete(notice)
                            db.session.commit()
                        #該USER為雇員
                        elif notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            noticeList.append({"content": "「{}」任務將在一小時後開始。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            noticeList.append({"content": "「{}」任務將在一小時後開始。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                    elif notice_.status == noticeType['taskStart']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 11:
                            db.session.delete(notice)
                            db.session.commit()
                        #該USER為雇員
                        elif notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            noticeList.append({"content": "「{}」任務開始，完成後請至雇員已通過頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            noticeList.append({"content": "「{}」任務開始，完成後請至雇主已接受頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                    elif notice_.status == noticeType['NoSP']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 12 or notice_.db_notice_noticeTask[0].task.SP == None:
                            db.session.delete(notice)
                            db.session.commit()
                        else:
                            noticeList.append({"content": "「{}」任務時間已到，仍無人承接，，可至歷史紀錄查看任務細節。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['taskEndTime']:
                        finished = False
                        for noticeTask_ in notice_.db_notice_noticeTask[0].task.db_task_noticeTask:
                            if noticeTask_.notice_.status == noticeType['taskFinish']:
                                finished = True
                                db.session.delete(notice)
                                db.session.commit()
                                break
                        if not Finished:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                noticeList.append({"content": "「{}」任務已結束。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                noticeList.append({"content": "「{}」任務已結束。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['createTask']:
                        noticeList.append({"content": "已成功功建立任務「{}」。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['cancelAccepting']:
                        noticeList.append({"content": "已收回您「{}」的任務申請。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SPPassed']:
                        noticeList.append({"content": "{}已接受您「{}」的任務申請，請至所有任務雇員已通過頁面查看。".format(\
                            notice_.db_notice_noticeTask[0].task.SR.name,\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SRCancel']:
                        noticeList.append({"content": "{}取消任務「{}」，若同意取消請至所有任務雇主已接受頁面點選取消，若不同意請忽略此訊息。".format(\
                            notice_.db_notice_noticeTask[0].task.SR.name,\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                    elif notice_.status == noticeType['SPCancel']:
                        noticeList.append({"content": "{}取消任務「{}」，若同意取消請至所有任務雇員已通過頁面點選取消，若不同意請忽略此則訊息".format(\
                            notice_.db_notice_noticeTask[0].task.SP.name,\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['cancelTask']:
                        #該USER為雇員
                        if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            noticeList.append({"content": "{}已同意取消任務「{}」，可至歷史紀錄查看任務細節。".format(\
                                notice_.db_notice_noticeTask[0].task.SR.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            noticeList.append({"content": "{}已同意取消任務「{}」，可至歷史紀錄查看任務細節。".format(\
                                notice_.db_notice_noticeTask[0].task.SP.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['deleteTask']:
                        noticeList.append({"content": "已成功刪除任務「{}」。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['editTask']:
                        noticeList.append({"content": "已成功編輯任務「{}」。".format(\
                            notice_.db_notice_noticeTask[0].task.taskName),\
                            "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SRFinish']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 13:
                            noticeList.append({"content": "「{}」{}已點選完成，請至雇員已通過頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SR.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        elif notice_.db_noticeTask[0].task.taskStatus == 14:
                            noticeList.append({"content": "「{}」{}已點選未完成，請至雇員已通過頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SR.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['SPFinish']:
                        if notice_.db_notice_noticeTask[0].task.taskStatus == 13:
                            noticeList.append({"content": "「{}」{}已點選完成，請至雇主已接受頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SP.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                        elif notice_.db_noticeTask[0].task.taskStatus == 14:
                            noticeList.append({"content": "「{}」{}已點選未完成，請至雇主已接受頁面點選完成。".format(\
                                notice_.db_notice_noticeTask[0].task.SP.name,\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                    elif notice_.status == noticeType['taskFinish']:
                        #該USER為雇員
                        if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                            noticeList.append({"content": "「{}」任務已結束。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                            noticeList.append({"content": "「{}」任務已結束。".format(\
                                notice_.db_notice_noticeTask[0].task.taskName),\
                                "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['pleaseComment']:
                        #還在評論狀態
                        if notice_.db_notice_noticeTask[0].task.db_task_comment[0].commentStatus == -1:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                if notice_.db_notice_noticeTask[0].task.db_task_comment[0].SPComment:
                                    noticeList.append({"content": "您尚未對「{}」評論，請至雇員已通過頁面評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskPassed'], "time": notice_.time})
                                else:
                                    db.session.delete(notice)
                                    db.session.commit()
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                if notice_.db_notice_noticeTask[0].task.db_task_comment[0].SRComment:
                                    noticeList.append({"content": "您尚未對「{}」評論，請至雇主已接受頁面評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskAccepted'], "time": notice_.time})
                                else:
                                    db.session.delete(notice)
                                    db.session.commit()
                        #進入審核狀態
                        else:
                            db.session.delete(notice)
                            db.session.commit()
                    elif notice_.status == noticeType['judgeComment']:
                        #評論通過
                        if notice_.db_notice_noticeTask[0].task.db_task_comment[0].commentStatus == 1:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                noticeList.append({"content": "管理員已通過您對「{}」的評論，可至歷史紀錄查看。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                noticeList.append({"content": "管理員已通過您對「{}」的評論，可至歷史紀錄查看。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                        #評論否決
                        elif notice_.db_notice_noticeTask[0].task.db_task_comment[0].commentStatus == 2:
                            #該USER為雇員
                            if notice_.db_notice_noticeTask[0].task.SP.userID == userID:
                                noticeList.append({"content": "管理員否決了您對「{}」的評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeTask[0].task.SR.userID == userID:
                                noticeList.append({"content": "管理員否決了您對「{}」的評論。".format(\
                                    notice_.db_notice_noticeTask[0].task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                elif notice_.db_notice_noticeCandidate:
                    noticeList.append({"content": "{}申請您的任務「{}」，請至所有任務雇主已發布頁面查看。".format(\
                                notice_.db_notice_noticeCandidate[0].taskCandidate.account.name,\
                                notice_.db_notice_noticeCandidate[0].taskCandidate.task.taskName),\
                                "connectTo": noticePage['SRAllTaskPassed'], "time": notice_.time})
                elif notice_.db_notice_noticeReport:
                    if notice_.status == noticeType['sendReport']:
                        #該USER為雇員
                        if notice_.db_notice_noticeReport[0].report.task.SP.userID == userID:
                            noticeList.append({"content": "「{}」任務的檢舉已送出，管理員正在為您處理。".format(\
                                notice_.db_notice_noticeReport[0].report.task.taskName),\
                                "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                        #該USER為雇主
                        elif notice_.db_notice_noticeReport[0].report.task.SR.userID == userID:
                            noticeList.append({"content": "「{}」任務的檢舉已送出，管理員正在為您處理。".format(\
                                notice_.db_notice_noticeReport[0].report.task.taskName),\
                                "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['judgeReport']:
                        #檢舉通過
                        if notice_.db_notice_noticeReport[0].report.reportStatus == 1:
                            #該USER為雇員
                            if notice_.db_notice_noticeReport[0].report.task.SP.userID == userID:
                                noticeList.append({"content": "「{}」任務的檢舉已通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeReport[0].report.task.SR.userID == userID:
                                noticeList.append({"content": "「{}」任務的檢舉已通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                        #檢舉未通過
                        elif notice_.db_notice_noticeReport[0].report.reportStatus == 2:
                            #該USER為雇員
                            if notice_.db_notice_noticeReport[0].report.task.SP.userID == userID:
                                noticeList.append({"content": "「{}」任務的檢舉未通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SPAllTaskRecord'], "time": notice_.time})
                            #該USER為雇主
                            elif notice_.db_notice_noticeReport[0].report.task.SR.userID == userID:
                                noticeList.append({"content": "「{}」任務的檢舉未通過，感謝您寶貴的意見。".format(\
                                    notice_.db_notice_noticeReport[0].report.task.taskName),\
                                    "connectTo": noticePage['SRAllTaskRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['judgeApply']:
                        #通過
                        if notice_.db_notice_noticeApply[0].apply.applyStatus == 1:
                            if notice_.db_notice_noticeApply[0].apply.result:
                                noticeList.append({"content": "點數申請{}：{}通過。".format(\
                                        notice_.noticeApply[0].apply.applyCondition.className,\
                                        notice_.noticeApply[0].apply.result),\
                                        "connectTo": noticePage['pointRecord'], "time": notice_.time})
                            else:
                                noticeList.append({"content": "點數申請{}通過。".format(\
                                        notice_.noticeApply[0].apply.applyCondition.className),\
                                        "connectTo": noticePage['pointRecord'], "time": notice_.time})
                        #未通過
                        elif notice_.db_notice_noticeApply[0].apply.applyStatus == 2:
                            #有原因
                            if notice_.db_notice_noticeApply[0].apply.result:
                                noticeList.append({"content": "點數申請{}：{}未通過。".format(\
                                    notice_.noticeApply[0].apply.applyCondition.className,\
                                    notice_.noticeApply[0].apply.result),\
                                    "connectTo": noticePage['pointRecord'], "time": notice_.time})
                            #沒有原因
                            else:
                                noticeList.append({"content": "點數申請{}未通過。".format(\
                                    notice_.noticeApply[0].apply.applyCondition.className),\
                                    "connectTo": noticePage['pointRecord'], "time": notice_.time})
                    elif notice_.status == noticeType['allotment']:
                        if notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.period == 0:
                            noticeList.append({"content": "管理員一次性配發了{}點給您。".format(\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.quota),\
                                "connectTo": noticePage['pointRecord'], "time": notice_.time})
                        else:
                            noticeList.append({"content": "管理員配發了{}點給您，{}/{}。".format(\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.quota,\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.times,\
                                notice_.db_notice_noticeAllotment[0].transferRecordAllotment.allotment.frequency),\
                                "connectTo": noticePage['pointRecord'], "time": notice_.time})
            return jsonify({"rspCode": "20", "noticeList": noticeList})             #成功取得通知
        else:
            return jsonify({"rspCode": "50"})                                           #權限不符
    else:
        return jsonify({"rspCode": "31"})                                           #method使用錯誤