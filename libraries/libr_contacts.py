import sqlite3, hashlib
from libraries.fgconfig import dataunit

def convhash(textobjc):
    textobjc = textobjc.encode("utf-8")
    texthash = hashlib.sha512(textobjc).hexdigest()
    return texthash

def chekexst(usercont, ownrname):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select usercont from contacts where ownrname = '" + str(ownrname) + "'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    contlist = []
    contexst = False
    for indx in recvobjc:
        contlist.apppend(indx[0])
    if usercont in contlist:
        contexst = True
    else:
        contexst = False
    return contexst

def addtocnt(usercont, ownrname):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    listiden = str(usercont) + "@" + str(ownrname)
    listiden = convhash(listiden)
    acticurs = database.cursor()
    qurytext = "insert into contacts values (" + \
               "'" + str(listiden) + "', " + \
               "'" + str(ownrname) + "', " + \
               "'" + str(usercont) + "') "
    acticurs.execute(qurytext)
    database.commit()
    database.close()

def delfmcnt(usercont, ownrname):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "delete from contacts where " + \
               "ownrname = '" + str(ownrname) + "' and " + \
               "usercont = '" + str(usercont) + "'"
    print(qurytext)
    acticurs.execute(qurytext)
    database.commit()
    database.close()

def fetccont(username):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select username, fullname from userdata where username in "+ \
               "(select usercont from contacts where ownrname = '" + str(username) + "')"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    usercoll = []
    for indx in range(len(recvobjc)):
        username = recvobjc[indx][0]
        fullname = recvobjc[indx][1]
        singcont = {
            "username": username,
            "fullname": fullname,
        }
        usercoll.append(singcont)
    database.close()
    return usercoll

def fetcsing(username):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select username, fullname, emailadr, digisign from userdata where username = '" + str(username) + "'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchone()
    signcont = {
        "username": recvobjc[0],
        "fullname": recvobjc[1],
        "emailadr": recvobjc[2],
        "digisign": recvobjc[3],
    }
    return signcont

def fetcuser(srchtext, username):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select username, fullname from userdata where username like '%" + str(srchtext) + "%' and " + \
               "username not in (select usercont from contacts where ownrname = '" + str(username) + "')"
    print(qurytext)
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    usercoll = []
    for indx in range(len(recvobjc)):
        username = recvobjc[indx][0]
        fullname = recvobjc[indx][1]
        signcont = {
            "username": username,
            "fullname": fullname,
        }
        usercoll.append(signcont)
    return usercoll
