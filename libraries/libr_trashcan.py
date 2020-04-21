import sqlite3, time, rsa
from libraries.libr_fgconfig import dataunit, timedata

def timeconv(timestmp):
    timelist = list(time.gmtime(timestmp))
    timedict = {
        "form": "GMT",
        "year": str(timelist[0]),
        "mont": timedata["montlist"][str(timelist[1])],
        "date": str(timelist[2]),
        "hour": str(timelist[3]),
        "mins": str(timelist[4]),
        "secs": str(timelist[5]),
        "wday": timedata["weeklist"][str(timelist[6])]
    }
    return timedict

def fetckeys(username):
    database = sqlite3.connect(dataunit["localuse"]["path"])
    acticurs = database.cursor()
    qurytext = "select prvkeynn, prvkeyee, prvkeydd, prvkeypp, prvkeyqq " + \
               "from settings where username = '" + str(username) + "'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    prvkeynn = int(recvobjc[0][0])
    prvkeyee = int(recvobjc[0][1])
    prvkeydd = int(recvobjc[0][2])
    prvkeypp = int(recvobjc[0][3])
    prvkeyqq = int(recvobjc[0][4])
    database.close()
    privtkey = rsa.PrivateKey(prvkeynn, prvkeyee, prvkeydd, prvkeypp, prvkeyqq)
    return privtkey

def fdecrypt(encstrim, privtkey):
    encstrim = encstrim.split("-")
    bytestrg = b""
    for indx in encstrim:
        if indx != "":
            bytestrg = bytestrg + bytes([int(indx)])
    try:
        decrbyte = rsa.decrypt(bytestrg, privtkey)
        decrstrg = decrbyte.decode("utf-8")
    except rsa.DecryptionError:
        decrstrg = "Message integrity compromised - Decryption failed!"
    return decrstrg

def fetcsend(username):
    privtkey = fetckeys(username)
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select mailiden, subjtext, conttext, destuser, timestmp from sendotoo where " + \
               "srceuser = '" + str(username) + "' and isitrmov = 'true'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    mailcoll = []
    for indx in range(len(recvobjc)):
        mailiden = recvobjc[indx][0]
        subjdecr = fdecrypt(recvobjc[indx][1], privtkey)
        contdecr = fdecrypt(recvobjc[indx][2], privtkey)
        destuser = recvobjc[indx][3]
        timeinfo = timeconv(float(recvobjc[indx][4]))
        singmail = {
            "subjtext": subjdecr, "conttext": contdecr,
            "destuser": destuser, "timedata": timeinfo,
            "mailiden": mailiden,
        }
        mailcoll.append(singmail)
    database.close()
    return mailcoll

def mailread(paradrct, mailiden, username):
    privtkey = fetckeys(username)
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = ""
    if paradrct == "send":
        qurytext = "select subjtext, conttext, destuser, timestmp from sendotoo where " + \
                   "mailiden = '" + str(mailiden) + "' and isitrmov = 'true'"
    elif paradrct == "recv":
        qurytext = "select subjtext, conttext, srceuser, timestmp from recvotoo where " + \
                   "mailiden = '" + str(mailiden) + "' and isitrmov = 'true'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    subjdecr = fdecrypt(recvobjc[0][0], privtkey)
    contdecr = fdecrypt(recvobjc[0][1], privtkey)
    interact = recvobjc[0][2]
    timeinfo = timeconv(float(recvobjc[0][3]))
    database.close()
    maildict = {
        "mailiden": mailiden, "timedata": timeinfo, "interact": interact,
        "subjtext": subjdecr, "conttext": contdecr,
    }
    return maildict

def moveinbx(paradrct, mailiden):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = ""
    if paradrct == "send":
        qurytext = "update sendotoo set isitrmov = 'false' where mailiden = '" + str(mailiden) + "'"
    elif paradrct == "recv":
        qurytext = "update recvotoo set isitrmov = 'false' where mailiden = '" + str(mailiden) + "'"
    acticurs.execute(qurytext)
    database.commit()
    database.close()

def purgemsg(paradrct, mailiden):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = ""
    if paradrct == "send":
        qurytext = "delete from sendotoo where mailiden = '" + str(mailiden) + "'"
    elif paradrct == "recv":
        qurytext = "delete from recvotoo where mailiden = '" + str(mailiden) + "'"
    acticurs.execute(qurytext)
    database.commit()
    database.close()

def fetcrecv(username):
    privtkey = fetckeys(username)
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select mailiden, subjtext, conttext, srceuser, timestmp from recvotoo where " + \
               "destuser = '" + str(username) + "' and isitrmov = 'true'"
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    mailcoll = []
    for indx in range(len(recvobjc)):
        mailiden = recvobjc[indx][0]
        subjdecr = fdecrypt(recvobjc[indx][1], privtkey)
        contdecr = fdecrypt(recvobjc[indx][2], privtkey)
        srceuser = recvobjc[indx][3]
        timeinfo = timeconv(float(recvobjc[indx][4]))
        singmail = {
            "subjtext": subjdecr, "conttext": contdecr,
            "srceuser": srceuser, "timedata": timeinfo,
            "mailiden": mailiden,
        }
        mailcoll.append(singmail)
    database.close()
    return mailcoll
