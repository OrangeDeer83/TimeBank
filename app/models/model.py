from . import db
import datetime

def partitionByTaskID(tasks, left, right):
    i = 0
    for j in range(right):
        if tasks[j].taskID < tasks[right].taskID:
            tasks[i], tasks[j] = tasks[j], tasks[i]
            i = i + 1
    tasks[right], tasks[i] = tasks[i], tasks[right]
    return i

#將task陣列sort
def sortTaskByTaskID(tasks, left, right):
    if left < right:
        privotLocation = partitionByTaskID(tasks, left, right)
        sortTaskByTaskID(tasks, left, privotLocation - 1)
        sortTaskByTaskID(tasks, privotLocation + 1, right)

def partitionByTaskStartTime(tasks, left, right):
    i = 0
    for j in range(right):
        if tasks[j].taskStartTime < tasks[right].taskStartTime:
            tasks[i], tasks[j] = tasks[j], tasks[i]
            i = i + 1
    tasks[right], tasks[i] = tasks[i], tasks[right]
    return i

#將task陣列sort
def sortTaskByTaskStartTime(tasks, left, right):
    if left < right:
        privotLocation = partitionByTaskStartTime(tasks, left, right)
        sortTaskByTaskID(tasks, left, privotLocation - 1)
        sortTaskByTaskID(tasks, privotLocation + 1, right)
        

taskSP = db.Table('taskSP', db.Column('taskID', db.Integer, db.ForeignKey('task.taskID')), db.Column('SPID', db.String(20), db.ForeignKey('account.userID')))

taskSR = db.Table('taskSR', db.Column('taskID', db.Integer, db.ForeignKey('task.taskID')), db.Column('SRID', db.String(20), db.ForeignKey('account.userID')))

class account(db.Model):
    __tablename__ = 'account'
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
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

    db_account_allotment = db.relationship('allotment', backref='account')
    db_account_apply = db.relationship('apply', backref='account')
    db_account_point = db.relationship('point', backref='account')
    db_account_pointRecord = db.relationship('pointRecord', backref='account')
    db_account_report = db.relationship('report', backref='account')
    db_account_taskCandidate = db.relationship('taskCandidate', backref='account')

    def __init__(self, userName, name, userPassword, userMail, userPhone, userInfo, userPoint, SRRate, SRRateTimes, SPRate, SPRateTimes, userGender, userBirthday, salt):
        self.userName = userName
        self.name = name
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
    adminID = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(20), nullable=False)
    adminPassword = db.Column(db.String, nullable=False)
    adminType = db.Column(db.Integer, nullable=False)
    adminPhone = db.Column(db.String(20), nullable=True)
    adminMail = db.Column(db.String(50), nullable=True)
    salt = db.Column(db.String(30), nullable=False)

    db_adminAccount_allotment = db.relationship('allotment', backref='adminAccount')
    db_adminAccount_apply = db.relationship('apply', backref='adminAccount')
    db_adminAccount_comment = db.relationship('comment', backref='adminAccount')
    db_adminAccount_point = db.relationship('point', backref='adminAccount')
    db_adminAccount_report = db.relationship('report', backref='adminAccount')

    def __init__(self, adminName, adminPassword, adminType, adminPhone, adminMail, salt):
        self.adminName = adminName
        self.adminPassword = adminPassword
        self.adminType = adminType
        self.adminPhone = adminPhone
        self.adminMail = adminMail
        self.salt = salt


class allotment(db.Model):
    __tablename__ = 'allotment'
    allotmentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), db.ForeignKey('account.userID'), nullable=False)
    allotmentStatus = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=True)
    restTime = db.Column(db.Integer, nullable=True)
    nextTime = db.Column(db.Integer, nullable=True)
    quota = db.Column(db.Integer, nullable=False)
    adminID = db.Column(db.String(20), db.ForeignKey('adminAccount.adminID'), nullable=False)
    allotmentTime = db.Column(db.DateTime, nullable = False)

    db_allotment_transferRecordAllotment = db.relationship('transferRecordAllotment', backref='allotment')

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
    adminID = db.Column(db.String(20), db.ForeignKey('adminAccount.adminID'), nullable=True)
    userID = db.Column(db.String(20), db.ForeignKey('account.userID'), nullable=True)
    conditionID = db.Column(db.Integer, db.ForeignKey('applyCondition.conditionID'), nullable=False)
    result = db.Column(db.String, nullable=True)
    applyTime = db.Column(db.DateTime, nullable=False)
    oldConditionID = db.Column(db.Integer, nullable=True)
    judgeTime = db.Column(db.DateTime, nullable=True)

    db_apply_noticeApply = db.relationship('noticeApply', backref='apply')
    db_apply_transferRecordApply = db.relationship('transferRecordApply', backref='apply')

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

    db_applyCondition_apply = db.relationship('apply', backref='applyCondition')

    def __init__(self, period, className, quota, available):
        self.period = period
        self.className = className
        self.quota = quota
        self.available = available


class comment(db.Model):
    __tablename__ = 'comment'
    commentID = db.Column(db.Integer, primary_key=True)
    taskID = db.Column(db.Integer, db.ForeignKey('task.taskID'), nullable=False, unique=True)
    SRComment = db.Column(db.String, nullable=True)
    SPComment = db.Column(db.String, nullable=True)
    commentStatus = db.Column(db.Integer, nullable=False)
    adminID = db.Column(db.String(20), db.ForeignKey('adminAccount.adminID'), nullable=True)

    def __init__(self, taskID, SRComment, SPComment, commentStatus, adminID):
        self.taskID = taskID
        self.SRComment = SRComment
        self.SPComment = SPComment
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


class notice(db.Model):
    __tablename__ = 'notice'
    ID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('account.userID'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    haveRead = db.Column(db.Integer, nullable=False)

    db_notice_noticeApply = db.relationship('noticeApply', backref='notice')
    db_notice_noticeCandidate = db.relationship('noticeCandidate', backref='notice')
    db_notice_noticeTask = db.relationship('noticeTask', backref='notice')
    db_notice_noticeReport = db.relationship('noticeReport', backref='notice')
    db_notice_noticeAllotment = db.relationship('noticeAllotment', backref='notice')

    def __init__(self, userID, time, status, haveRead):
        self.userID = userID
        self.time = time
        self.status = status
        self.haveRead = haveRead


class noticeApply(db.Model):
    __tablename__ = 'noticeApply'
    ID = db.Column(db.Integer, primary_key=True)
    noticeID = db.Column(db.Integer, db.ForeignKey('notice.ID'), nullable=False)
    applyID = db.Column(db.Integer, db.ForeignKey('apply.applyID'), nullable=False)

class noticeCandidate(db.Model):
    __tablename__ = 'noticeCandidate'
    ID = db.Column(db.Integer, primary_key=True)
    noticeID = db.Column(db.Integer, db.ForeignKey('notice.ID'), nullable=False)
    candidateID = db.Column(db.Integer, db.ForeignKey('taskCandidate.rejectID'), nullable=False)

    def __init__(self, noticeID, candidateID):
        self.noticeID = noticeID
        self.candidateID = candidateID


class noticeAllotment(db.Model):
    __tablename__ = 'noticeAllotment'
    ID = db.Column(db.Integer, primary_key=True)
    noticeID = db.Column(db.Integer, db.ForeignKey('notice.ID'), nullable=False)
    transferRecordAllotmentID = db.Column(db.Integer, db.ForeignKey('transferRecordAllotment.transferRecordAllotmentID'), nullable=False)

    def __init__(self, noticeID, transferRecordAllotmentID):
        self.noticeID = noticeID
        self.transferRecordAllotmentID = transferRecordAllotmentID


class noticeReport(db.Model):
    __tablename__ = 'noticeReport'
    ID = db.Column(db.Integer, primary_key=True)
    noticeID = db.Column(db.Integer, db.ForeignKey('notice.ID'), nullable=False)
    reportID = db.Column(db.Integer, db.ForeignKey('report.reportID'), nullable=False)

    def __init__(self, noticeID, reportID):
        self.noticeID = noticeID
        self.reportID = reportID


class noticeTask(db.Model):
    __tablename__ = 'noticeTask'
    ID = db.Column(db.Integer, primary_key=True)
    noticeID = db.Column(db.Integer, db.ForeignKey('notice.ID'), nullable=False)
    taskID = db.Column(db.Integer, db.ForeignKey('task.taskID'), nullable=False)
    
    def __init__(self, noticeID, taskID):
        self.noticeID = noticeID
        self.taskID = taskID


class point(db.Model):
    __tablename__ = 'point'
    pointID = db.Column(db.String(50), primary_key=True)
    adminID = db.Column(db.String(20), db.ForeignKey('adminAccount.adminID'), nullable=False)
    ownerID = db.Column(db.String(20), db.ForeignKey('account.userID'), nullable=False)

    db_point_pointRecord = db.relationship('pointRecord', backref='point')

    def __init__(self, pointID, adminID, ownerID):
        self.pointID = pointID
        self.adminID = adminID
        self.ownerID = ownerID


class pointRecord(db.Model):
    __tablename__ = 'pointRecord'
    pointRecordID = db.Column(db.Integer, primary_key=True)
    pointID = db.Column(db.String(50), db.ForeignKey('point.pointID'), nullable=False, unique=True)
    ownerID = db.Column(db.String(20), db.ForeignKey('account.userID'), nullable=False)
    transferTime = db.Column(db.DateTime, nullable=False)

    def __init__(self, pointID, ownerID, transferTime):
        self.pointID = pointID
        self.ownerID = ownerID
        self.transferTime = transferTime


class report(db.Model):
    __tablename__ = 'report'
    reportID = db.Column(db.Integer, primary_key=True)
    taskID = db.Column(db.Integer, db.ForeignKey('task.taskID'), nullable=False)
    adminID = db.Column(db.String(20), db.ForeignKey('adminAccount.adminID'), nullable=True)
    reason = db.Column(db.String, nullable=False)
    reportStatus = db.Column(db.Integer, nullable=False)
    reportUserID = db.Column(db.String(20), db.ForeignKey('account.userID'), nullable=False)
    
    db_report_noticeReport = db.relationship('noticeReport', backref='report')

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
    SP = db.relationship('account', secondary=taskSP, backref='taskSP')
    SR = db.relationship('account', secondary=taskSR, backref='taskSR')

    db_task_comment = db.relationship('comment', backref='task')
    db_task_report = db.relationship('report', backref='task')
    db_task_taskCandidate = db.relationship('taskCandidate', backref='task')
    db_task_transferRecordTask = db.relationship('transferRecordTask', backref='task')
    db_task_noticeTask = db.relationship('noticeTask', backref='task')

    def __init__(self, taskName, taskContent, taskPoint, taskLocation, taskStartTime, taskEndTime, taskStatus):
        self.taskName = taskName
        self.taskContent = taskContent
        self.taskPoint = taskPoint
        self.taskLocation =taskLocation
        self.taskStartTime =taskStartTime
        self.taskEndTime = taskEndTime
        self.taskStatus = taskStatus


class taskCandidate(db.Model):
    __tablename__ = 'taskCandidate'
    rejectID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), db.ForeignKey('account.userID'), nullable=False)
    taskID = db.Column(db.Integer, db.ForeignKey('task.taskID'), nullable=False)

    db_taskCandidate_noticeCandidate = db.relationship('noticeCandidate', backref='taskCandidate')

    def __init__(self, userID, taskID):
        self.userID =userID
        self.taskID =taskID

class transferRecord(db.Model):
    __tablename__ = 'transferRecord'
    transferRecordID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('account.userID'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    db_transferRecord_transferRecordAllotment = db.relationship('transferRecordAllotment', backref='transferRecord')
    db_transferRecord_transferRecordApply = db.relationship('transferRecordApply', backref='transferRecord')
    db_transferRecord_transferRecordTask = db.relationship('transferRecordTask', backref='transferRecord')

    def __init__(self, userID, time):
        self.userID = userID
        self.time = time


class transferRecordAllotment(db.Model):
    __tablename__ = 'transferRecordAllotment'
    transferRecordAllotmentID = db.Column(db.Integer, primary_key=True)
    transferRecordID = db.Column(db.Integer, db.ForeignKey('transferRecord.transferRecordID'), nullable=False)
    allotmentID = db.Column(db.Integer, db.ForeignKey('allotment.allotmentID'), nullable=False)
    times = db.Column(db.Integer, nullable=False)

    db_transferRecordAllotment_noticeAllotment = db.relationship('noticeAllotment', backref='transferRecordAllotment')

    def __init__(self, transferRecordID, allotmentID, times):
        self.transferRecordID = transferRecordID
        self.allotmentID = allotmentID
        self.times = times


class transferRecordApply(db.Model):
    __tablename__ = 'transferRecordApply'
    transferRecordApplyID = db.Column(db.Integer, primary_key=True)
    transferRecordID = db.Column(db.Integer, db.ForeignKey('transferRecord.transferRecordID'), nullable=False)
    applyID = db.Column(db.Integer, db.ForeignKey('apply.applyID'), nullable=False)
    times = db.Column(db.Integer, nullable=False)

    def __init__(self, transferRecordID, applyID, times):
        self.transferRecordID = transferRecordID
        self.applyID = applyID
        self.times = times


class transferRecordTask(db.Model):
    __tablename__ = 'transferRecordTask'
    transferRecordTaskID = db.Column(db.Integer, primary_key=True)
    transferRecordID = db.Column(db.Integer, db.ForeignKey('transferRecord.transferRecordID'), nullable=False)
    taskID = db.Column(db.Integer, db.ForeignKey('task.taskID'), nullable=False)

    def __init__(self, transferRecordID, taskID):
        self.transferRecordID = transferRecordID
        self.taskID = taskID