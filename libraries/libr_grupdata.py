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

def grupexst(grupname):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select grupname from grupinfo where grupname = '" + str(grupname) + "'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchone()
    if recvobjc is None:
        return False
    else:
        return True

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

def savegrup(grupname, partlist, username):
    grupiden = convhash(grupname)
    rsabuild = generate()
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "insert into grupinfo values (" + \
               "'" + str(grupiden) + "', " + \
               "'" + str(grupname) + "', " + \
               "'" + str(username) + "', " + \
               "'" + str(rsabuild["publckey"]["n"]) + "', " + \
               "'" + str(rsabuild["publckey"]["e"]) + "') "
    acticurs.execute(qurytext)
    userlist = []
    for indx in partlist:
        idengenr = indx + grupiden
        identity = convhash(idengenr)
        userdict = {
            "identity": identity,
            "username": indx,
        }
        userlist.append(userdict)
    for indx in userlist:
        qurytext = "insert into grupteam values (" + \
                   "'" + str(indx["identity"]) + "', " + \
                   "'" + str(grupiden) + "', " + \
                   "'" + str(indx["username"]) + "')"
        try:
            acticurs.execute(qurytext)
        except:
            pass
    database.commit()
    database.close()
    database = sqlite3.connect(dataunit["localuse"]["path"])
    acticurs = database.cursor()
    for indx in userlist:
        qurytext = "insert into gruploca values (" + \
                   "'" + str(indx["identity"]) + "', " + \
                   "'" + str(grupiden) + "', " + \
                   "'" + str(rsabuild["publckey"]["n"]) + "', " + \
                   "'" + str(rsabuild["publckey"]["e"]) + "', " + \
                   "'" + str(rsabuild["privtkey"]["n"]) + "', " + \
                   "'" + str(rsabuild["privtkey"]["e"]) + "', " + \
                   "'" + str(rsabuild["privtkey"]["d"]) + "', " + \
                   "'" + str(rsabuild["privtkey"]["p"]) + "', " + \
                   "'" + str(rsabuild["privtkey"]["q"]) + "') "
        try:
            acticurs.execute(qurytext)
        except:
            pass
    database.commit()
    database.close()
    return grupiden

def listfetc(username):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select * from grupinfo where grupiden in " + \
               "(select grupiden from grupteam where username = " + \
               "'" + str(username) + "')"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    gruplist = []
    for indx in recvobjc:
        grupdict = {
            "grupiden": indx[0],
            "grupname": indx[1],
            "ownrname": indx[2],
        }
        gruplist.append(grupdict)
    database.close()
    return gruplist