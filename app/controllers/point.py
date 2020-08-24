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