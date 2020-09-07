import pymysql, re, os
from app.models import hash

def empty(data):
    if data:
        return False
    return True

def create_account():
    db = pymysql.connect("192.168.1.147", "root", "root", "timeBankTest")
    cursor = db.cursor()

    cursor.execute("SELECT adminName FROM adminAccount WHERE adminType = '7'")
    data = cursor.fetchone()
    print(data)
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
        choose = input("已經存在一個超級管理者帳號「{}」請問是否要將他刪除並建立新帳號(yes/no): ".format(data[0]))
        while choose != "yes" and choose != "no":
            choose = input("請輸入yes或no來確認是否建立新帳號: ")
        if choose == "yes":
            cursor.execute("DELETE FROM adminAccount WHERE adminType = '7'")
            db.commit()
            adminName = account_repeat(cursor)
            sql = enter_info(adminName)
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
    adminName = input("請輸入想要創建的新帳號（不可大於20個字元，且不得有符號）: ")
   
    while re.search(r"^[\w\d]{1,20}$", adminName) == None:
        adminName = input("帳號不得大於20個字元，且不得有符號！!\n請重新輸入新帳號: ")
    cursor.execute("SELECT adminID FROM adminAccount WHERE adminName = '" + adminName + "'")
    data = cursor.fetchone()
    while not empty(data):
        adminID = input("帳號重複了！\n請重新輸入新帳號（不可大於20個字元，且不得有符號）: ")
        while re.search(r"^[\w\d]{1,20}$", adminName) == None:
            adminID = input("帳號不得大於20個字元，且不得有符號！!\n請重新輸入新帳號: ")
        cursor.execute("SELECT adminID FROM adminAccount WHERE adminID = '" + adminName + "'")
        data = cursor.fetchone()
    return adminName

def enter_info(adminName):
    adminPassword = input("請輸入您的密碼（8至20個字元，須包含至少1個大寫、1個小寫、1個數字、1個符號）: ")
    while re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,30}$", adminPassword) == None:
        adminPassword = input("密碼不符合規範！\n請重新輸入您的密碼（8至20個字元，須包含至少1個大寫、1個小寫、一個數字、一個符號）:")
    salt = hash.generate_salt()
    sql = "INSERT INTO adminAccount(adminName, adminPassword, adminType, salt) "
    sql += "VALUES('" + str(adminName) + "', '" + str(hash.encrypt(adminPassword, salt)) + "', '7', '" + str(salt) + "')"
    print(sql)
    return sql

if __name__ == "__main__":
    create_account()