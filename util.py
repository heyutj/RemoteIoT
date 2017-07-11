import json
import hashlib
def reg(user_name,  password):
    if(len(user_name)>8):
        raise 'password error' 
    data = {
    'version':'1.0', 
    'method': 'REG', 
    'username': str(user_name), 
    'password': hashlib.md5(password.encode('ascii')).hexdigest()
    }
    return json.dumps(data)

def login(userid,  password):
    data = {
    'version':'1.0', 
    'method': 'LOGIN', 
    'username': str(userid), 
    'password': hashlib.md5(password.encode('ascii')).hexdigest()
    }
    return json.dumps(data)
def ping(userid,  session):
    data = {
    'version':'1.0', 
    'method': 'PING', 
    'userid': str(userid), 
    'session': session
    }
    return json.dumps(data)
def userlist(userid,  session):
    data = {
    'version':'1.0', 
    'method': 'USERLIST', 
    'userid': str(userid), 
    'session': session
    }
    return json.dumps(data)
def addfriend(userid,  session,  userid_add):
    data = {
    'version':'1.0', 
    'method': 'ADDFRIEND', 
    'session': session, 
    'userid': str(userid), 
    'request': str(userid_add)
    }
    return json.dumps(data)
def delfriend(userid,  session,  userid_del):
    data = {
    'version':'1.0', 
    'method': 'DELFRIEND',  
    'session': session, 
    'userid': str(userid), 
    'request': str(userid_del)
    }
    return json.dumps(data)
    
def listfriend(userid,  session):
    data = {
    'version':'1.0', 
    'method': 'LISTFRIEND', 
    'userid': str(userid), 
    'session': session, 
    }
    return json.dumps(data)
def get_topic(userid,  session,  request):
    data = {
    'version':'1.0', 
    'method': 'CHAT', 
    'userid': str(userid), 
    'request': request, 
    'session': session, 
    }
    return json.dumps(data)
