from flask import Blueprint, render_template, session, jsonify, request
from ..models.model import *
from ..models import userType
from math import floor

Profile = Blueprint('profile', __name__)

#取得個人資料
@Profile.route('/output', methods=['GET'])
def output():
    if request.method == 'GET':
        if session.get('userType') == userType['USER']:
            userID = session('userID')
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