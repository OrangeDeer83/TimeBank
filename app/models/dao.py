from .hash import *
import datetime
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
    return "INSERT INTO `applyCondition` (`period`, `className`, `quota`,`available`) VALUES ('{}', '{}', '{}',1)".format(period,className,quota)

def list_alive_apply_className():
    return "SELECT DISTINCT className FROM `applyCondition` WHERE `className` != '其他' AND `available` != 0 ORDER BY className "

def show_quota_by_period_className_alive(className,period):
    return "SELECT quota FROM `applyCondition` WHERE `className` LIKE '{}' AND `available` != 0 AND `period` = {}".format(className,period)

def let_apply_condition_die(className):
    return "UPDATE `applyCondition` SET available = 0 WHERE className = '{}'".format(className)

def let_apply_condition_die_className_period(className,period):
    return "UPDATE `applyCondition` SET available = 0 WHERE className ='{}' AND period ={}".format(className,period)

def show_quota_conditionID_by_className_period(className,period):
    return "SELECT `conditionID`, `quota` FROM `applyCondition` WHERE `className` = '{}' AND `period` ={} AND `available` = 1".format(className,period)

def out_put_allow_period(className):#
    return "SELECT `period` FROM `applyCondition` WHERE `className` = '{}' AND `available` = 1 ORDER BY period".format(className)

def show_conditionID(className,period):#
    return "SELECT `conditionID` FROM `applyCondition` WHERE `className` = '{}' AND `period` ={} AND `available` = 1".format(className,period)

def set_up_apply_condition(className,period,quota):#
    return "INSERT INTO `applyCondition` (`period`, `className`, `quota`, `available`) VALUES ('{}', '{}', '{}', '1')".format(period,className,quota)

def find_other_apply_condition_id(period,quota):#
    return "SELECT `conditionID` FROM `applyCondition` where `className` LIKE '其他' AND `period` = {} AND `quota` = {}".format(period,quota)

def add_apply(frequency,restTime,nextTime,userID,conditionID,result,time):
    return "INSERT INTO `apply` (`applyID`, `applyStatus`, `frequency`, `restTime`, `nextTime`, `adminID`, `userID`, `conditionID`, `result`, `applyTime`) VALUES (NULL, '0', '{}', '{}', '{}', NULL, '{}', '{}', '{}', '{}')".format(frequency,restTime,nextTime,userID,conditionID,result,time)

def find_max_applyId_by_user_ID(userID):
    return "SELECT MAX(`applyID`) FROM apply WHERE userID LIKE '{}'".format(userID)

def get_all_apply_status_0():
    return "SELECT `applyID`,`userID`,`conditionID`,`applyTime`,`result`,`frequency` FROM `apply` WHERE `applyStatus` = 0 ORDER BY applyID"

def get_apply_judge_user_info(userID):
    return "SELECT `name`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes`, `userName`, `userPoint`FROM `account` WHERE `userID` = '{}'".format(userID)


def show_condition_data(conditionID):
    return "SELECT `period`,`className`,`quota` FROM `applyCondition` WHERE `conditionID` ='{}'".format(conditionID)

def alter_apply_status(status,applyID):
    return "UPDATE `apply` SET `applyStatus` = '{}' WHERE `apply`.`applyID` = {}".format(status,applyID)

def set_up_special_apply_condition(className,period,quota):
    return "INSERT INTO `applyCondition` (`period`, `className`, `quota`, `available`) VALUES ('{}', '{}', '{}', '0')".format(period,className,quota)

def get_conditionID(applyID):
    return "SELECT conditionID FROM apply WHERE applyID = {}".format(applyID)

def find_special_apply_condition(className,period,quota):
    return "SELECT `conditionID` FROM `applyCondition` where `className` LIKE '{}' AND `period` = {} AND `quota` = {}".format(className,period,quota)

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
    return "SELECT `period`,`className`,`quota` FROM `applyCondition` WHERE `conditionID` ='{}'".format(conditionID)

def update_judge_time_in_apply(judgeTime,applyID):
    return "UPDATE `apply` SET `judgeTime` = '{}' WHERE `apply`.`applyID` = {}".format(judgeTime,applyID)

def select_user_name(userID):
    return "SELECT name FROM account WHERE userID = '{}'".format(userID)

def get_all_apply_status_0_search_user_name(userName):
    return 'SELECT apply.applyID,apply.userID,apply.conditionID,apply.applyTime,apply.result,apply.frequency FROM apply JOIN account WHERE apply.applyStatus = 0 AND apply.userID=account.userID AND (account.userName LIKE "{}" OR account.name LIKE "{}") ORDER BY applyID'.format(userName,userName)

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
        sql += "AND applyCondition.className = '{}'".format(className)
    if userName != "":
        sql += "AND ( account.userName = '{}' OR account.name = '{}')".format(userName,userName)
    return sql

def select_all_user():
    return "SELECT `userID`,`name`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes`,`userPoint`FROM `account` ORDER BY userID"

def select_search_user(target):
    return "SELECT `userID`,`name`,`SRRate`,`SRRateTimes`,`SPRate`,`SPRateTimes`,`userPoint` FROM `account` WHERE name = '{}' OR userName = '{}' ORDER BY userID".format(target,target)

def add_allotment(userID,frequency,period,quota,adminID,allotmentTime):
    return "INSERT INTO `allotment` (`allotmentID`, `userID`, `allotmentStatus`, `frequency`, `period`, `restTime`, `nextTime`, `quota`, `adminID`, `allotmentTime`) VALUES (NULL, '{}', '1', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(userID,frequency,period,str(int(period)*int(frequency)),period,quota,adminID,allotmentTime)

def select_search_userID(target):
    if target != '':
        return "SELECT `userID` FROM `account` WHERE name = '{}' OR userName = '{}' ORDER BY userID".format(target,target)
    else:
        return "SELECT `userID` FROM `account` ORDER BY userID"

def select_allotment_simple_history_by_userID(userID= ''):
    if userID != '':
        return "SELECT allotmentTime, quota, period, frequency FROM allotment WHERE userID = '{}' ORDER BY allotmentID DESC".format(userID)
    else:
        return "SELECT allotmentTime, quota, period, frequency FROM allotment ORDER BY allotmentID DESC"

def select_allotment_history_by_userID_userName(userID = '',name=''):
    if userID != '' and name != '':
        return "SELECT allotmentTime, quota, period, frequency,account.userID,account.name,SRRate,SRRateTimes,SPRate,SPRateTimes FROM allotment JOIN account WHERE allotment.userID = account.userID AND (allotment.userID = '{}' OR account.name = '{}') ORDER BY allotmentID DESC".format(userID,name)
    else:
        return "SELECT allotmentTime, quota, period, frequency, account.userID, account.name, SRRate, SRRateTimes, SPRate, SPRateTimes FROM allotment JOIN account WHERE allotment.userID = account.userID ORDER BY allotmentID DESC"
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

def make_point_sql(pointID,adminID,userID,time_):
    return "INSERT INTO `point` (`pointID`, `adminID`, `ownerID`, `time`) VALUES ('{}', '{}', '{}','{}')".format(pointID,adminID,userID,time_)

def show_rest_time_by_applyID(applyID):
    return "SELECT restTime FROM apply WHERE applyID ='{}'".format(applyID)

def alter_apply_rest_time(applyID,rest):
    return "UPDATE `apply` SET `restTime` = '{}' WHERE `apply`.`applyID` = {}".format(rest,applyID)

def task_status_4_dead_line(task_ID,newTaskStartTime):
    return "CREATE EVENT `task_status_4_dead_line-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN UPDATE `task` SET `taskStatus` = '4' WHERE `task`.`taskID` = {} AND (`task`.`taskStatus` = 0 OR `task`.`taskStatus` = 1); DROP EVENT `task_status_4_dead_line-{}`; END;".format(task_ID,newTaskStartTime,task_ID,task_ID)

def drop_task_status_4_dead_line(task_ID):
    return "DROP EVENT `task_status_4_dead_line-{}`;".format(task_ID)

def thing_will_do_while_task_endTime_plus_1h(task_ID,newTaskEndTime):
    sql = "CREATE EVENT `thing_will_do_while_task_endTime_plus_1h-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN ".format(task_ID,newTaskEndTime)
    sql = sql + "UPDATE `task` SET `taskStatus` = '5' WHERE `task`.`taskID` = {} AND (`task`.`taskStatus` = 2 OR `task`.`taskStatus` = 9 OR `task`.`taskStatus` = 10); ".format(task_ID)
    sql = sql + "UPDATE `task` SET `taskStatus` = '6' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 15 ;".format(task_ID)
    sql = sql + "UPDATE `task` SET `taskStatus` = '5' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 2; ".format(task_ID)
    sql = sql + "UPDATE `task` SET `taskStatus` = '3' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 16;".format(task_ID)
    sql = sql + "UPDATE `task` SET `taskStatus` = '7' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 14; ".format(task_ID)
    sql = sql + "UPDATE `task` SET `taskStatus` = '3' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 16; ".format(task_ID)
    sql = sql + "DROP EVENT `thing_will_do_while_task_endTime_plus_1h-{}`; END;".format(task_ID)
    return sql

def drop_thing_will_do_while_task_endTime_plus_1h(task_ID):
    return "DROP EVENT `thing_will_do_while_task_endTime_plus_1h-{}`;".format(task_ID)

def comment_status_0(task_ID,EndTime):
    return "CREATE EVENT `comment_status_0-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN UPDATE `comment` SET `commentStatus` = '0' WHERE `comment`.`taskID` = {} AND `comment`.`commentStatus` = -1 AND NOT(`comment`.`SRComment` is NULL AND `comment`.`SPComment` is NULL); DROP EVENT `comment_status_0-{}`; END;".format(task_ID,EndTime,task_ID,task_ID)

def drop_comment_status_0(task_ID):
    return "DROP EVENT `comment_status_0-{}`;".format(task_ID)

def task_status_15_to_6(task_ID,newTaskEndTime):
    return "CREATE EVENT `task_status_15_to_6-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN UPDATE `task` SET `taskStatus` = '6' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 15 ; DROP EVENT `task_status_15_to_6-{}`; END;".format(task_ID,newTaskEndTime,task_ID,task_ID)

def task_status_2_to_5(task_ID,newTaskEndTime):
    return "CREATE EVENT `task_status_2_to_5-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN UPDATE `task` SET `taskStatus` = '5' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 2; DROP EVENT `task_status_2_to_5-{}`; END;".format(task_ID,newTaskEndTime,task_ID,task_ID)

def task_status_16_to_3(task_ID,newTaskEndTime):
    return "CREATE EVENT `task_status_16_to_3-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN UPDATE `task` SET `taskStatus` = '3' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 16; DROP EVENT `task_status_16_to_3-{}`; END;".format(task_ID,newTaskEndTime,task_ID,task_ID)

def task_status_14_to_7(task_ID,newTaskEndTime):
    return "CREATE EVENT `task_status_14_to_7-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN UPDATE `task` SET `taskStatus` = '7' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 14; DROP EVENT `task_status_14_to_7-{}`; END;".format(task_ID,newTaskEndTime,task_ID,task_ID)

def task_status_13_to_3(task_ID,newTaskEndTime):
    return "CREATE EVENT `task_status_13_to_3-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN UPDATE `task` SET `taskStatus` = '3' WHERE `task`.`taskID` = {} AND `task`.`taskStatus` = 13; DROP EVENT `task_status_13_to_3-{}`; END;".format(task_ID,newTaskEndTime,task_ID,task_ID)

def task_will_start(SRID,taskID_,taskStartTime,SPID):
    return "CREATE EVENT `task_will_start-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '9', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}');INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '9', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}'); DROP EVENT `task_will_start-{}`; END;".format(taskID_,taskStartTime,SRID,taskStartTime,taskID_,SPID,taskStartTime,taskID_,taskID_)

def task_start(userID_,taskID_,taskStartTime,SPID):
    return "CREATE EVENT `task_start-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '10', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}');INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '10', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}'); DROP EVENT `task_start-{}`; END;".format(taskID_,taskStartTime,userID_,taskStartTime,taskID_,SPID,taskStartTime,taskID_,taskID_)

def NoSP(userID_,taskID_,taskStartTime):
    return "CREATE EVENT `NoSP-{}-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '11', '0');   SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO `noticeTask` (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}'); DROP EVENT `NoSP-{}-{}`; END;".format(taskID_,userID_,taskStartTime,userID_,taskStartTime,taskID_,taskID_,userID_)

def drop_NoSP(taskID_,userID_):
    return " DROP EVENT `NoSP-{}-{}`;".format(taskID_,userID_)


def plzComment(userID_,taskID_,taskStartTime,SPID):	
    return "CREATE EVENT `plzComment-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '17', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}'); INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '17', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}');DROP EVENT `plzComment-{}`; END;".format(taskID_,taskStartTime,userID_,taskStartTime,taskID_,SPID,taskStartTime,taskID_,taskID_)

def taskEndTime_sql(userID_,taskID_,taskEndTime,SPID):
    return "CREATE EVENT `taskEndTime-{}` ON SCHEDULE AT '{}' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '21', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}'); INSERT INTO `notice` (`ID`, `userID`, `time`, `status`, `haveRead`) VALUES (NULL, '{}', '{}', '21', '0');SET @noticeID = ( SELECT MAX(ID) FROM notice);  INSERT INTO noticeTask (`ID`, `noticeID`, `taskID`) VALUES (NULL, @noticeID, '{}'); DROP EVENT `taskEndTime-{}`; END;".format(taskID_,taskEndTime,userID_,taskEndTime,taskID_,SPID,taskEndTime,taskID_,taskID_)



