import sqlite3, hashlib, rsa
from libraries.libr_fgconfig import dataunit

def acntexst(username):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select username from userdata"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    userlist = []
    for indx in recvobjc:
        userlist.append(indx[0])
    database.close()
    if username in userlist:
        return True
    else:
        return False

def convhash(password,username):
    password = password.encode("utf-8")
    username = username.encode("utf-8")
    passhash = hashlib.sha512(password).hexdigest()
    userhash = hashlib.sha512(username).hexdigest()
    return passhash, userhash

def generate():
    publckey, privtkey = rsa.newkeys(2048)
    publclst = str(publckey)[10:-1].split(",")
    privtlst = str(privtkey)[11:-1].split(",")
    keyepair = {
        "publckey" : {
            "n" : int(publclst[0]),
            "e" : int(publclst[1])
        },
        "privtkey" : {
            "n" : int(privtlst[0]),
            "e" : int(privtlst[1]),
            "d" : int(privtlst[2]),
            "p" : int(privtlst[3]),
            "q" : int(privtlst[4])
        }
    }
    print(keyepair)
    return keyepair

def saveuser(fullname,username,password,emailadr):
    passhash, digisign = convhash(password,username)
    rsabuild = generate()
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "insert into userdata values (" + \
               "'" + str(username) + "', " + \
               "'" + str(passhash) + "', " + \
               "'" + str(fullname) + "', " + \
               "'" + str(emailadr) + "', " + \
               "'" + str(digisign) + "', " + \
               "'" + str(rsabuild["publckey"]["n"]) + "', " + \
               "'" + str(rsabuild["publckey"]["e"]) + "')"
    print(qurytext)
    acticurs.execute(qurytext)
    database.commit()
    database.close()
    database = sqlite3.connect(dataunit["localuse"]["path"])
    acticurs = database.cursor()
    qurytext = "insert into settings values (" + \
               "'" + str(username) + "', " + \
               "'" + str(digisign) + "', " + \
               "'" + str(rsabuild["publckey"]["n"]) + "', " + \
               "'" + str(rsabuild["publckey"]["e"]) + "', " + \
               "'" + str(rsabuild["privtkey"]["n"]) + "', " + \
               "'" + str(rsabuild["privtkey"]["e"]) + "', " + \
               "'" + str(rsabuild["privtkey"]["d"]) + "', " + \
               "'" + str(rsabuild["privtkey"]["p"]) + "', " + \
               "'" + str(rsabuild["privtkey"]["q"]) + "') "
    print(qurytext)
    acticurs.execute(qurytext)
    database.commit()
    database.close()
    return digisign
