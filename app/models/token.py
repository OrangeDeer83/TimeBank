from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

def create_token(key, userID, timeout):
    s = TimedJSONWebSignatureSerializer(key, timeout)
    token = s.dumps({"userID": userID})
    return token

def validate_token(key, token):
    s = TimedJSONWebSignatureSerializer(key)
    try:
        data = s.loads(bytes(token, encoding="utf-8"))
    except SignatureExpired:
        print("Time out")
        return False
    except BadSignature:
        print("BadSignature")
        return False
    print("驗證成功")
    return data