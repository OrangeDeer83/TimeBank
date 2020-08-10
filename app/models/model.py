#print("model.py在", __name__)
from . import db


class account(db.Model):
    __tablename__ = 'account'
    userID = db.Column(db.String(20, collation='CASE'), primary_key=True)
    userName = db.Column(db.String(20), nullable=False)
    userPassword = db.Column(db.String, nullable=False)
    userMail = db.Column(db.String(50), nullable=False)
    userPhone = db.Column(db.String(20), nullable=False)
    userInfo = db.Column(db.String, nullable=True)
    userPoint = db.Column(db.Integer, nullable=False)
    SRRate = db.Column(db.Integer, nullable=True)
    SRRateTimes = db.Column(db.Integer, nullable=False)
    SPRate = db.Column(db.Integer, nullable=True)
    SPRateTimes = db.Column(db.Integer, nullable=False)
    userGender = db.Column(db.Integer, nullable=False)
    userBirthday = db.Column(db.DateTime, nullable=False)
    salt = db.Column(db.String, nullable=False)


    def __init__(self, userID, userName, userPassword, userMail, userPhone, userInfo, userPoint, SRRate, SRRateTimes, SPRate, SPRateTimes, userGender, userBirthday, salt):
        self.userID = userID
        self.userName = userName
        self.userPassword = userPassword
        self.userMail = userMail
        self.userPhone = userPhone
        self.userInfo = userInfo
        self.userPoint = userPoint
        self.SRRate = SRRate
        self.SRRateTimes = SRRateTimes
        self.SPRate = SPRate
        self.SPRateTimes = SPRateTimes
        self.userGender = userGender
        self.userBirthday = userBirthday
        self.salt = salt


class adminAccount(db.Model):
    __tablename__ = 'adminAccount'
    adminID = db.Column(db.String(20), primary_key=True)
    adminName = db.Column(db.String(20), nullable=False)
    adminPassword = db.Column(db.String, nullable=False)
    adminType = db.Column(db.Integer, nullable=False)
    adminPhone = db.Column(db.String(20), nullable=True)
    adminMail = db.Column(db.String(50), nullable=True)
    salt = db.Column(db.String(30), nullable=False)

    def __init__(self, adminID, adminName, adminPassword, adminType, adminPhone, adminMail, salt):
        self.adminID = adminID
        self.adminName = adminName
        self.adminPassword = adminPassword
        self.adminType = adminType
        self.adminPhone = adminPhone
        self.adminMail = adminMail
        self.salt = salt


class allotment(db.Model):
    __tablename__ = 'allotment'
    allotmentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), nullable=False)
    allotmentStatus = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=True)
    restTime = db.Column(db.Integer, nullable=True)
    nextTime = db.Column(db.Integer, nullable=True)
    quota = db.Column(db.Integer, nullable=False)
    adminID = db.Column(db.String(20), nullable=False)
    allotmentTime = db.Column(db.DateTime, nullable = False)

    def __init__(self, userID, allotmentStatus, frequency, period, restTime, nextTime, quota, adminID, allotmentTime):
        self.userID = userID
        self.allotmentStatus = allotmentStatus
        self.frequency = frequency
        self.period = period
        self.restTime = restTime
        self.nextTime = nextTime
        self.quota = quota
        self.adminID = adminID
        self.allotmentTime = allotmentTime



class apply(db.Model):
    __tablename__ = 'apply'
    applyID = db.Column(db.Integer, primary_key=True)
    applyStatus = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    restTime = db.Column(db.Integer, nullable=True)
    nextTime = db.Column(db.Integer, nullable=True)
    adminID = db.Column(db.String(20), nullable=True)
    userID = db.Column(db.String(20), nullable=True)
    conditionID = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String, nullable=True)
    applyTime = db.Column(db.DateTime, nullable=False)
    oldConditionID = db.Column(db.Integer, nullable=True)
    judgeTime = db.Column(db.DateTime, nullable=True)

    def __init__(self, applyStatus, frequency, restTime, nextTime, adminID, userID, conditionID, result, applyTime, oldConditionID, judgeTime):
        self.applyStatus = applyStatus
        self.frequency = frequency
        self.restTime = restTime
        self.nextTime = nextTime
        self.adminID = adminID
        self.userID = userID
        self.conditionID = conditionID
        self.result = result
        self.applyTime = applyTime
        self.oldConditionID = oldConditionID
        self.judgeTime = judgeTime

class applyCondition(db.Model):
    __tablename__ = 'applyCondition'
    conditionID = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer, nullable=False)
    className = db.Column(db.String(10), nullable=False)
    quota = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)

    def __init__(self, period, className, quota, available):
        self.period = period
        self.className = className
        self.quota = quota
        self.available = available

class comment(db.Model):
    __tablename__ = 'comment'
    commentID = db.Column(db.Integer, primary_key=True)
    taskID = db.Column(db.Integer, nullable=False, unique=True)
    SRComment = db.Column(db.String, nullable=False)
    SPComment = db.Column(db.String, nullable=False)
    commentDeadline = db.Column(db.DateTime, nullable=False)
    commentStatus = db.Column(db.Integer, nullable=False)
    adminID = db.Column(db.String(20), nullable=True)

    def __init__(self, taskID, SRComment, SPComment, commentDeadline, commentStatus, adminID):
        self.taskID = taskID
        self.SRComment = SRComment
        self.SPComment = SPComment
        self.commentDeadline = commentDeadline
        self.commentStatus = commentStatus
        self.adminID = adminID

class news(db.Model):
    __tablename__ = 'news'
    newsID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    newsTime = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, newsTime):
        self.title = title
        self.newsTime = newsTime

class point(db.Model):
    __tablename__ = 'point'
    pointID = db.Column(db.String(50), primary_key=True)
    adminID = db.Column(db.String(20), nullable=False)
    ownerID = db.Column(db.String(20), nullable=False)

    def __init__(self, pointID, adminID, ownerID):
        self.pointID = pointID
        self.adminID = adminID
        self.ownerID = ownerID

class pointRecord(db.Model):
    __tablename__ = 'pointRecord'
    pointRecordID = db.Column(db.Integer, primary_key=True)
    pointID = db.Column(db.String(50), nullable=False, unique=True)
    ownerID = db.Column(db.String(20), nullable=False)
    transferTime = db.Column(db.DateTime, nullable=False)

    def __init__(self, pointID, ownerID, transferTime):
        self.pointID = pointID
        self.ownerID = ownerID
        self.transferTime = transferTime

class report(db.Model):
    __tablename__ = 'report'
    reportID = db.Column(db.Integer, primary_key=True)
    taskID = db.Column(db.Integer, nullable=False)
    adminID = db.Column(db.String(20), nullable=True)
    reason = db.Column(db.String, nullable=False)
    reportStatus = db.Column(db.Integer, nullable=False)
    reportUserID = db.Column(db.String(20), nullable=False)
    
    def __init__(self, taskID, adminID, reason, reportStatus, reportUserID):
        self.taskID = taskID
        self.adminID = adminID
        self.reason = reason
        self.reportStatus = reportStatus
        self.reportUserID = reportUserID

class task(db.Model):
    __tablename__ = 'task'
    taskID = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.String(20), nullable=False)
    taskContent = db.Column(db.String, nullable=False)
    taskPoint = db.Column(db.Integer, nullable=False)
    taskLocation = db.Column(db.String, nullable=False)
    taskStartTime = db.Column(db.DateTime, nullable=False)
    taskEndTime = db.Column(db.DateTime, nullable=False)
    taskStatus = db.Column(db.Integer, nullable=False)
    SRID = db.Column(db.String(20), nullable=False)
    SPID = db.Column(db.String(20), nullable=True)

    def __init__(self,SPID, taskName, taskContent,SRID, taskPoint, taskLocation, taskStartTime, taskEndTime, taskStatus):
        self.taskName = taskName
        self.taskContent = taskContent
        self.taskPoint = taskPoint
        self.taskLocation =taskLocation
        self.taskStartTime =taskStartTime
        self.taskEndTime = taskEndTime
        self.taskStatus = taskStatus
        self.SPID =SPID
        self.SRID =SRID

class taskCandidate(db.Model):
    __tablename__ = 'taskCandidate'
    rejectID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), nullable=False)
    taskID = db.Column(db.Integer, nullable=False)

    def __init__(self, userID, taskID):
        self.userID =userID
        self.taskID =taskID    