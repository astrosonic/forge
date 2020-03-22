import hashlib

trgtuser = {
    "username" : None,
    "digisign" : None
}

def convhash(username):
    username = username.encode("utf-8")
    userhash = hashlib.sha512(username).hexdigest()
    return userhash

def makesess(username):
    digisign = convhash(username)
    trgtuser["username"] = username
    trgtuser["digisign"] = digisign
    return trgtuser

def valdsess(username):
    if username == trgtuser["username"]:
        return True
    else:
        return False

def rmovsess(username):
    return None