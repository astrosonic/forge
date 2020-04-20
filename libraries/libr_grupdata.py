import sqlite3, hashlib, time, rsa
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

def grupexst(grupiden):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select grupiden from grupinfo"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    gruplist = []
    for indx in recvobjc:
        gruplist.append(indx[0])
    database.close()
    if grupiden in gruplist:
        return True
    else:
        return False

def convhash(idengenr):
    idengenr = idengenr.encode("utf-8")
    hashotpt = hashlib.sha512(idengenr).hexdigest()
    return hashotpt

def doesexst(partlist):
    for indx in partlist:
        if acntexst(indx) is True:
            pass
        else:
            return False
    return True

def fetcgrup(grupiden):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select grupname, ownrname from grupinfo where grupiden='" + str(grupiden) + "'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchone()
    grupname = recvobjc[0]
    ownrname = recvobjc[1]
    qurytext = "select username from grupteam where grupiden='" + str(grupiden) + "'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    userlist = []
    for indx in recvobjc:
        userlist.append(indx[0])
    database.close()
    retndata = {
        "grupiden": grupiden,
        "grupname": grupname,
        "ownrname": ownrname,
        "userlist": userlist,
    }
    return retndata

def savegrup(grupname, partlist, username):
    timecurt = str(time.time())
    idengenr = grupname + timecurt
    grupiden = convhash(idengenr)
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "insert into grupinfo values (" + \
               "'" + str(grupiden) + "', " + \
               "'" + str(grupname) + "', " + \
               "'" + str(username) + "')"
    acticurs.execute(qurytext)
    for indx in partlist:
        idengenr = indx + grupiden
        identity = convhash(idengenr)
        qurytext = "insert into grupteam values (" + \
                   "'" + str(identity) + "', " + \
                   "'" + str(grupiden) + "', " + \
                   "'" + str(indx) + "')"
        print(qurytext)
        try:
            acticurs.execute(qurytext)
        except:
            pass
    database.commit()
    database.close()
    return grupiden

def listgrup(username):
    pass