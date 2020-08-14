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

def forgot_password(userMail):
    sql = "SELECT userID, userMail FROM account WHERE userMail = '" + userMail + "'"
    return sql

def reset_USER_password(userID, userPassword):
    salt = generate_salt()
    sql = "UPDATE account SET salt = '" + str(salt) + "', userPassword = '" + str(encrypt(userPassword, salt)) + "' WHERE userIDdaw = '" + str(userID) + "'"
    return sql
'''


def max_newsID():
    return "SELECT MAX(newsID) FROM news"

def insert_news(title,time):
    return "INSERT INTO `news` (`newsID`, `title`, `newsTime`) VALUES (NULL, '{}', '{}')".format(title,time)

def select_title(number):
    return "SELECT title FROM news WHERE newsID = {} ORDER BY newsID DESC".format(number)

def update_title(title,number):
    return "UPDATE `news` SET `title` = '{}' WHERE `news`.`newsID` = {}".format(title,number)

def delete_news_(number):
    return "DELETE FROM `news` WHERE `news`.`newsID` = {}".format(number)

def add_apply_condition(period,className,quota):
    return "INSERT INTO `applyCondition` (`period`, `class`, `quota`,`available`) VALUES ('{}', '{}', '{}',1)".format(period,className,quota)

def list_alive_apply_class():
    return "SELECT DISTINCT class FROM `applyCondition` WHERE `class` != '其他' AND `available` != 0 ORDER BY class "

def show_quota_by_period_class_alive(className,period):
    return "SELECT quota FROM `applyCondition` WHERE `class` LIKE '{}' AND `available` != 0 AND `period` = {}".format(className,period)

def let_apply_condition_die(className):
    return "UPDATE `applyCondition` SET available = 0 WHERE class = '{}'".format(className)

def let_apply_condition_die_class_period(className,period):
    return "UPDATE `applyCondition` SET available = 0 WHERE class ='{}' AND period ={}".format(className,period)

def show_quota_conditionID_by_class_period(className,period):
    return "SELECT `conditionID`, `quota` FROM `applyCondition` WHERE `class` = '{}' AND `period` ={} AND `available` = 1".format(className,period)

def out_put_allow_period(className):#
    return "SELECT `period` FROM `applyCondition` WHERE `class` = '{}' AND `available` = 1 ORDER BY period".format(className)

def show_conditionID(className,period):#
    return "SELECT `conditionID` FROM `applyCondition` WHERE `class` = '{}' AND `period` ={} AND `available` = 1".format(className,period)

def set_up_apply_condition(className,period,quota):#
    return "INSERT INTO `applyCondition` (`period`, `class`, `quota`, `available`) VALUES ('{}', '{}', '{}', '1')".format(period,className,quota)

def find_other_apply_condition_id(period,quota):#
    return "SELECT `conditionID` FROM `applyCondition` where `class` LIKE '其他' AND `period` = {} AND `quota` = {}".format(period,quota)

def add_apply(frequency,restTime,nextTime,userID,conditionID,result,time):
    return "INSERT INTO `apply` (`applyID`, `applyStatus`, `frequency`, `restTime`, `nextTime`, `adminID`, `userID`, `conditionID`, `result`, `applyTime`) VALUES (NULL, '0', '{}', '{}', '{}', NULL, '{}', '{}', '{}', '{}')".format(frequency,restTime,nextTime,userID,conditionID,result,time)

def find_max_applyId_by_user_ID(userID):
    return "SELECT MAX(`applyID`) FROM apply WHERE userID LIKE '{}'".format(userID)

def get_all_apply_status_0():
    return "SELECT `applyID`,`userID`,`conditionID`,`applyTime`,`result`,`frequency` FROM `apply` WHERE `applyStatus` = 0 ORDER BY applyID"

def get_apply_judge_user_info(userID):
    return "SELECT `userName`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes`FROM `account` WHERE `userID` = '{}'".format(userID)

def show_condition_data(conditionID):
    return "SELECT `period`,`class`,`quota` FROM `applyCondition` WHERE `conditionID` ='{}'".format(conditionID)

def alter_apply_status(status,applyID):
    return "UPDATE `apply` SET `applyStatus` = '{}' WHERE `apply`.`applyID` = {}".format(status,applyID)

def set_up_special_apply_condition(className,period,quota):
    return "INSERT INTO `applyCondition` (`period`, `class`, `quota`, `available`) VALUES ('{}', '{}', '{}', '0')".format(period,className,quota)

def get_conditionID(applyID):
    return "SELECT conditionID FROM apply WHERE applyID = {}".format(applyID)

def find_special_apply_condition(className,period,quota):
    return "SELECT `conditionID` FROM `applyCondition` where `class` LIKE '{}' AND `period` = {} AND `quota` = {}".format(className,period,quota)

def alter_conditionID_in_apply(conditionID,applyID):
    return "UPDATE `apply` SET `conditionID` = '{}' WHERE `apply`.`applyID` = {}".format(conditionID,applyID)

def get_userID_by_applyID(applyID):
    return "SELECT userID FROM apply where applyID = {}".format(applyID)

def alter_oldConditionID(conditionID,applyID):
    return "UPDATE `apply` SET `oldConditionID` = '{}' WHERE `apply`.`applyID` = {}".format(conditionID,applyID)

def upudate_adminID_in_apply(adminID,applyID):
    return "UPDATE `apply` SET `adminID` = '{}' WHERE `apply`.`applyID` = {}".format(adminID,applyID)

def find_all_judged_apply_by_userID(userID,applyID):
    return "SELECT conditionID ,applyTime,frequency,result,applyStatus,oldConditionID,judgeTime,applyID FROM apply WHERE userID LIKE '{}' AND applyStatus != 0 AND applyID !={} ORDER BY applyID DESC".format(userID,applyID)

def select_quota_by_conditionID(conditionID):
    return "SELECT quota FROM applyCondition WHERE conditionID = '{}'".format(conditionID)

def show_old_condition_data(conditionID):
    return "SELECT `period`,`class`,`quota` FROM `applyCondition` WHERE `conditionID` ='{}'".format(conditionID)

def update_judge_time_in_apply(judgeTime,applyID):
    return "UPDATE `apply` SET `judgeTime` = '{}' WHERE `apply`.`applyID` = {}".format(judgeTime,applyID)

def select_user_name(userID):
    return "SELECT userName FROM account WHERE userID = '{}'".format(userID)

def get_all_apply_status_0_search_user_name(userName):
    return 'SELECT apply.applyID,apply.userID,apply.conditionID,apply.applyTime,apply.result,apply.frequency FROM apply JOIN account WHERE apply.applyStatus = 0 AND apply.userID=account.userID AND (account.userName = "{}" OR account.name = "{}") ORDER BY applyID'.format(userName,userName)

def show_judge_history(userName = "",className = "" , period = "" , status = ""):
    sql = "SELECT apply.conditionID ,applyTime,frequency,result,applyStatus,oldConditionID,judgeTime,applyID,apply.userID FROM apply JOIN account,applyCondition WHERE apply.applyStatus != 0 AND apply.conditionID = applyCondition.conditionID AND apply.userID =account.userID "
    if userName == None and className == None and period == None and status == None:
        sql += "ORDER BY apply.applyID DESC"
        return sql
    if status != "":
        sql += "AND apply.applyStatus = '{}' ".format(status)
    if period != "":
        sql += "AND applyCondition.period = '{}'".format(period)
    if className!= "":
        sql += "AND applyCondition.class = '{}'".format(className)
    if userName != "":
        sql += "AND ( account.userName = '{}' OR account.name = '{}')".format(userName,userName)
    return sql

def select_all_user():
    return "SELECT `userID`,`userName`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes`FROM `account` ORDER BY userID"

def select_search_user(target):
    return "SELECT `userID`,`userName`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes` FROM `account` WHERE name = '{}' OR userName = '{}' ORDER BY userID".format(target,target)

def add_allotment(userID,frequency,period,quota,adminID,allotmentTime):
    return "INSERT INTO `allotment` (`allotmentID`, `userID`, `allotmentStatus`, `frequency`, `period`, `restTime`, `nextTime`, `quota`, `adminID`, `allotmentTime`) VALUES (NULL, '{}', '1', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(userID,frequency,period,str(int(period)*int(frequency)),period,quota,adminID,allotmentTime)

def select_search_userID(target):
    if target != '':
        return "SELECT `userID` FROM `account` WHERE name = '{}' OR userName = '{}' ORDER BY userID".format(target,target)
    else:
        return "SELECT `userID` FROM `account` ORDER BY userID"

def select_allotment_simple_history_by_userID(userID= ''):
    if userID != '':
        return "SELECT allotmentTime, quota, period, frequency FROM allotment WHERE userID = '{}' ORDER BY allotmentID DESC'".format(userID)
    else:
        return "SELECT allotmentTime, quota, period, frequency FROM allotment ORDER BY allotmentID DESC"

def select_allotment_history_by_userID_userName(userID = '',userName=''):
    if userID != '' and userName != '':
        return "SELECT allotmentTime, quota, period, frequency,account.userID,account.userName,SRRate,SRRateTimes,SPRate,SPRateTimes FROM allotment JOIN account WHERE allotment.userID = account.userID AND (allotment.userID = '{}' OR account.userName = '{}') ORDER BY allotmentID DESC".format(userID,userName)
    else:
        return "SELECT allotmentTime, quota, period, frequency, account.userID, account.userName, SRRate, SRRateTimes, SPRate, SPRateTimes FROM allotment JOIN account WHERE allotment.userID = account.userID ORDER BY allotmentID DESC"

def check_point_ID(pointID):
    return "SELECT pointID FROM point WHERE pointID = '{}'".format(pointID)

def find_max_allotmentID_by_adminID(adminID):
    return "SELECT MAX(`allotmentID`) FROM `allotment` WHERE adminID ='{}'".format(adminID)

def show_rest_time_by_alomentID(allotmentID):
    return "SELECT restTime FROM allotment WHERE allotmentID ='{}'".format(allotmentID)

def alter_allotment_rest_time(allotmentID,rest):
    return "UPDATE `allotment` SET `restTime` = '{}' WHERE `allotment`.`allotmentID` = {}".format(rest,allotmentID)

def get_user_point(userID):
    return "SELECT `userPoint` FROM `account` WHERE userID = '{}'".format(userID)

def plus_user_point(plus,userID):
    return "UPDATE `account` SET `userPoint` = '{}' WHERE `account`.`userID` = '{}'".format(plus,userID)

def make_point_sql(pointID,adminID,userID):
    return "INSERT INTO `point` (`pointID`, `adminID`, `ownerID`) VALUES ('{}', '{}', '{}')".format(pointID,adminID,userID)

def show_rest_time_by_applyID(applyID):
    return "SELECT restTime FROM apply WHERE applyID ='{}'".format(applyID)

def alter_apply_rest_time(applyID,rest):
    return "UPDATE `apply` SET `restTime` = '{}' WHERE `apply`.`applyID` = {}".format(rest,applyID)

def task_status_4_dead_line(task_ID,newTaskStartTime):
    return "CREATE EVENT `task_status_4_dead_line-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE `task` SET `taskStatus` = '4' WHERE `task`.`taskID` = {} AND (`task`.`taskStatus` = 0 OR `task`.`taskStatus` = 1)".format(task_ID,newTaskStartTime,task_ID)

def task_status_5_dead_line(task_ID,newTaskEndTime):
    return "CREATE EVENT `task_status_5_dead_line-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE `task` SET `taskStatus` = '5' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 2".format(task_ID,newTaskEndTime,task_ID)
