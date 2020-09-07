from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

def USER_forgot_password_token(key, userID):
    s = TimedJSONWebSignatureSerializer(key, 300)
    token = s.dumps({"userID": userID})
    return token

def Admin_forgot_password_token(key, adminID):
    s = TimedJSONWebSignatureSerializer(key, 300)
    token = s.dumps({"adminID": adminID})
    return token

def GM_forgot_password_token(key, GMID):
    s = TimedJSONWebSignatureSerializer(key, 300)
    token = s.dumps({"GMID": GMID})
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
        return "TimeOut"
    except BadSignature:
        return False
    return data