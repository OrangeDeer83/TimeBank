#coding:utf-8
import hashlib, random

def encrypt(data, salt):
    s = hashlib.sha256()
    #鹽的第15個為偶數就反轉密碼
    if ord(salt[15]) % 2 == 0:
        data = data[::-1]
    #在密碼中加入鹽
    data = data[:int(len(data) / 2)] + salt + data[int(len(data) / 2):]
    s.update(data.encode("utf-8"))
    h = s.hexdigest()
    return h

#產生鹽
def generate_salt():
    salt = ""
    i = 0
    while i < 30:
        i += 1
        num = random.randint(42, 122)
        while  num == 92:
            num = random.randint(42,122)
        salt += chr(num)
    return salt

#檢查密碼是否相同
def check_same(password, encrypted_password, salt):
    if (encrypt(password, salt) == encrypted_password):
        return True
    return False

if __name__ == "__main__":
    print(encrypt("1234567890", generate_salt()))