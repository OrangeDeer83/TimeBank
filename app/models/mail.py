#coding: utf-8
from flask import url_for
import smtplib
from email.mime.text import MIMEText

reset_password = "點擊以下連結以重設密碼\nhttp://192.168.1.146:5000"

#一般使用者密碼重置信
def USER_forgot_password_mail(token, mail):
    mime = MIMEText(reset_password + url_for('USER.reset_password', token=token), "plain", "utf-8")          #內文
    mime["Subject"] = "TimeBank - 重設密碼"                                                                 #標題
    #mime["From"] = "steven200083@gmail.com"                                                                #寄件人
    mime["To"] = mail                                                                                       #收件人
    msg = mime.as_string()                                                                                  #轉字串
    #設定SMTP
    smtp=smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.ehlo()
    smtp.login('steven200083@gmail.com','ftwrjrytoeqjnuib')
    from_addr = 'noreply@timeBank.com'
    to_addr = mail
    status = smtp.sendmail(from_addr, to_addr, msg)
    smtp.quit()
    return status

#管理員密碼重置信
def Admin_forgot_password_mail(token, mail):
    mime = MIMEText(reset_password + url_for('Admin.reset_password', token=token), "plain", "utf-8")         #內文
    mime["Subject"] = "TimeBank - 重設密碼"                                                                 #標題
    #mime["From"] = "steven200083@gmail.com"                                                                #寄件人
    mime["To"] = mail                                                                                       #收件人
    msg = mime.as_string()                                                                                  #轉字串
    #設定SMTP
    smtp=smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.ehlo()
    smtp.login('steven200083@gmail.com','ftwrjrytoeqjnuib')
    from_addr = 'noreply@timeBank.com'
    to_addr = mail
    status = smtp.sendmail(from_addr, to_addr, msg)
    smtp.quit()
    return status

#管理員密碼重置信
def GM_forgot_password_mail(token, mail):
    mime = MIMEText(reset_password + url_for('GM.reset_password', token=token), "plain", "utf-8")            #內文
    mime["Subject"] = "TimeBank - 重設密碼"                                                                 #標題
    #mime["From"] = "steven200083@gmail.com"                                                                #寄件人
    mime["To"] = mail                                                                                       #收件人
    msg = mime.as_string()                                                                                  #轉字串
    #設定SMTP
    smtp=smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.ehlo()
    smtp.login('steven200083@gmail.com','ftwrjrytoeqjnuib')
    from_addr = 'noreply@timeBank.com'
    to_addr = mail
    status = smtp.sendmail(from_addr, to_addr, msg)
    smtp.quit()
    return status

def GM_verify_mail(token, mail):
    mime = MIMEText("點擊以下連結以驗證帳號\nhttp://192.168.1.146:5000" +\
                    url_for('account.GM_verify', token=token), "plain", "utf-8")                #內文
    mime["Subject"] = "TimeBank - 評論管理員驗證信"                                              #標題
    #mime["From"] = "steven200083@gmail.com"                                                    #寄件人
    mime["To"] = mail                                                                           #收件人
    msg = mime.as_string()                                                                      #轉字串
    #設定SMTP
    smtp=smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('steven200083@gmail.com','itzqgclbfpojylmw')
    from_addr = 'noreply@timeBank.com'
    to_addr = mail
    status = smtp.sendmail(from_addr, to_addr, msg)
    smtp.quit()
    return status