from .hash import *

def empty(data):
    for i in data:
        if i:
            return False
    return True

def detect_repeated(userID):
    sql = "SELECT * FROM account WHERE userID = '" + userID + "'"
    #sql = "SELECT * FROM adminAccount WHERE userID = '" + userID + "'"
    return sql
'''
def register_1(name, id, password, mail, phone, gender, birthday):
    sql = "INSERT INTO account(userName, userID, userPassword, userMail, userPhone, userGender, userBirthday) VALUES('"
    sql += name + "', '" + id + "', '" + encrypt(password) + "', '" + mail + "', '" + phone + "', '" + gender + "', '" + birthday + "')"
    return sql

def register(userData):
    salt = generate_salt()
    sql = "INSERT INTO account(userName, userID, userPassword, userMail, userPhone, userGender, userBirthday, userPoint, SRRateTimes, SPRateTimes, salt) VALUES('"
    sql += str(userData[0]) + "', '" + str(userData[1]) + "', '" + str(encrypt(userData[2], salt)) + "', '" + str(userData[3]) + "', '" + str(userData[4]) + "', '" + str(userData[5]) + "', '" + str(userData[6]) + "', '0', '0', '0', '" + salt + "')"
    return sql


def login_user(userID):
    sql = "SELECT userID, userPassword, salt FROM account WHERE userID = '" + userID + "'"
    return sql

def forget_password(userMail):
    sql = "SELECT userID, userMail FROM account WHERE userMail = '" + userMail + "'"
    return sql

def reset_user_password(userID, userPassword):
    salt = generate_salt()
    sql = "UPDATE account SET salt = '" + str(salt) + "', userPassword = '" + str(encrypt(userPassword, salt)) + "' WHERE userIDdaw = '" + str(userID) + "'"
    return sql
'''