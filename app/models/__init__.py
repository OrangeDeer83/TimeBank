from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(use_native_unicode = 'utf8')

'''
GM狀態:     SA填寫Email | GM註冊 | GM點擊驗證連結 |  名稱
                1           0           0         unverify
                0           1           0           apply
                0           1           1         waiting
'''
userType = {'STOP': 0, 'USER': 1, 'AS': 2, 'AA': 3, 'AU': 4, 'AG': 5, 'GM': 6,
            'SA': 7, 'USER_unverify': 8, 'AS_unverify': 9, 'AA_unverify': 10,
            'AU_unverify': 11, 'AG_unverify': 12, 'GM_unverify': 13, 'SA_unverify': 14,
            'GM_apply': 15, 'GM_waiting': 16}