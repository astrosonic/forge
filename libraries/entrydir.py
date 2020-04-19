import sqlite3, hashlib
from libraries.fgconfig import dataunit

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

def convhash(password):
    password = password.encode("utf-8")
    passhash = hashlib.sha512(password).hexdigest()
    return passhash

def chekuser(username,password):
    passhash = convhash(password)
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select passhash from userdata where " + \
               "username = '" + str(username) + "'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    passrecv = recvobjc[0][0]
    database.close()
    if passrecv == passhash:
        return True
    else:
        return False