from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

def user_forget_password_token(key, userID):
    s = TimedJSONWebSignatureSerializer(key, 300)
    token = s.dumps({"userID": userID})
    return token

def GM_verify_token(key, GMID):
    s = TimedJSONWebSignatureSerializer(key, 300)
    token = s.dumps({"GMID": GMID})
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
    return data

