import pymysql, re, os
from app.models import hash

def empty(data):
    if data:
        return False
    return True

def create_account():
    db = pymysql.connect("192.168.1.147", "root", "root", "testTimeBank")
    cursor = db.cursor()

    cursor.execute("SELECT adminID FROM adminAccount WHERE adminType = '7'")
    data = cursor.fetchone()

    if empty(data):
        adminID = account_repeat(cursor)
        sql = enter_info(adminID)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print("帳號創建失敗，請重啟再試")
            os.system("PAUSE")
            exit()
        print("帳號創建成功")
        os.system("PAUSE")
        exit()
    else:
        choose = input("已經存在一個超級管理者帳號'{}'請問是否要將他刪除並建立新帳號(yes/no): ".format(data[0]))
        while choose != "yes" and choose != "no":
            choose = input("請輸入yes或no來確認是否建立新帳號: ")
        if choose == "yes":
            cursor.execute("DELETE FROM adminAccount WHERE adminType = '7'")
            db.commit()
            adminID = account_repeat(cursor)
            sql = enter_info(adminID)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print("帳號創建失敗，請重啟再試")
                os.system("PAUSE")
                exit()
            print("帳號創建成功")
            os.system("PAUSE")
            exit()
        else:
            print("取消創建帳號，準備離開程式")
            os.system("PAUSE")
            exit()
    db.close()
    


def account_repeat(cursor):
    adminID = input("請輸入想要創建的新帳號（不可大於20個字元，且不得有符號）: ")
   
    while re.search(r"^[\w\d]{1,20}$", adminID) == None:
        adminID = input("帳號不得大於20個字元，且不得有符號！!\n請重新輸入新帳號: ")
    cursor.execute("SELECT adminID FROM adminAccount WHERE adminID = '" + adminID + "'")
    data = cursor.fetchone()
    while not empty(data):
        adminID = input("帳號重複了！\n請重新輸入新帳號（不可大於20個字元，且不得有符號）: ")
        while re.search(r"^[\w\d]{1,20}$", adminID) == None:
            adminID = input("帳號不得大於20個字元，且不得有符號！!\n請重新輸入新帳號: ")
        cursor.execute("SELECT adminID FROM adminAccount WHERE adminID = '" + adminID + "'")
        data = cursor.fetchone()
    return adminID

def enter_info(adminID):
    adminName = input("請為新的帳號取一個名稱（不可大於20個字元）: ")
    while re.search(r"^.{1,20}$", adminName) == None:
        adminName = input("名稱長度不符合規範！\n請重新輸入新帳號的名稱（不可大於20個字元）: ")
    adminPassword = input("請輸入您的密碼（8至20個字元，須包含至少1個大寫、1個小寫、1個數字、1個符號）: ")
    while re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", adminPassword) == None:
        adminPassword = input("密碼不符合規範！\n請重新輸入您的密碼（8至20個字元，須包含至少1個大寫、1個小寫、一個數字、一個符號）:")
    adminPhone = input("請輸入您的電話: ")
    while re.search(r"^[0-9]+$", adminPhone) == None:
        adminPhone = input("電話請輸入數字！\t/請重新輸入電話: ")
    adminMail = input("請輸入您的信箱: ")
    while re.search(r"^[\w\d_\-\.]+\@[\w\d_\-\.]+\.[\w]$", adminMail):
        adminMail = input("信箱有誤，請重新輸入正確的信箱: ")
    salt = hash.generate_salt()
    sql = "INSERT INTO adminAccount(adminID, adminName, adminPassword, adminType, adminPhone, adminMail, salt) "
    sql += "VALUES('" + str(adminID) + "', '" + str(adminName) + "', '" + str(hash.encrypt(adminPassword, salt)) + "', '7', '" + str(adminPhone) + "', '" + str(adminMail) + "', '" + str(salt) + "')"
    print(sql)
    return sql

if __name__ == "__main__":
    create_account()