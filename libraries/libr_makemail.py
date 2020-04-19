import sqlite3, hashlib, time, rsa
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

def convhash(textobjc):
    textobjc = textobjc.encode("utf-8")
    texthash = hashlib.sha512(textobjc).hexdigest()
    return texthash

def fetckeys(username):
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "select pubkeynn, pubkeyee from userdata where username = '" + str(username) + "'";
    recvobjc = acticurs.execute(qurytext)
    recvobjc = recvobjc.fetchall()
    pubkeynn = int(recvobjc[0][0])
    pubkeyee = int(recvobjc[0][1])
    database.close()
    publckey = rsa.PublicKey(pubkeynn, pubkeyee)
    return publckey

def fencrypt(textobjc, publckey):
    textbyte = textobjc.encode("utf-8")
    textencr = rsa.encrypt(textbyte, publckey)
    encrstrg = ""
    for indx in textencr:
        encrstrg = encrstrg + str(indx) + "-"
    return encrstrg

def sendmail(subjtext, conttext, srceuser, destuser):
    isitrmov = "false"
    timestmp = str(time.time())
    pubkeysd = fetckeys(srceuser)                   # Fetches the sender's public key for storing in SENT MAIL
    subjensd = fencrypt(subjtext, pubkeysd)         # Encrypts the SUBJECT with sender's public key for SENT MAIL
    contensd = fencrypt(conttext, pubkeysd)         # Encrypts the CONTENT with sender's public key for SENT MAIL
    pubkeyrc = fetckeys(destuser)                   # Fetches the receiver's public key for SENDING
    subjenrc = fencrypt(subjtext, pubkeyrc)         # Encrypts the SUBJECT with receiver's public key for SENDING
    contenrc = fencrypt(conttext, pubkeyrc)         # Encrypts the CONTENT with receiver's public key for SENDING
    textobjc = subjtext + "@" + timestmp
    mailiden = convhash(textobjc)
    database = sqlite3.connect(dataunit["clouduse"]["path"])
    acticurs = database.cursor()
    qurytext = "insert into sendotoo values (" + \
               "'" + str(mailiden) + "', " + \
               "'" + str(subjensd) + "', " + \
               "'" + str(contensd) + "', " + \
               "'" + str(srceuser) + "', " + \
               "'" + str(destuser) + "', " + \
               "'" + str(timestmp) + "', " + \
               "'" + str(isitrmov) + "') "
    acticurs.execute(qurytext)
    database.commit()
    qurytext = "insert into recvotoo values (" + \
               "'" + str(mailiden) + "', " + \
               "'" + str(subjenrc) + "', " + \
               "'" + str(contenrc) + "', " + \
               "'" + str(srceuser) + "', " + \
               "'" + str(destuser) + "', " + \
               "'" + str(timestmp) + "', " + \
               "'" + str(isitrmov) + "') "
    acticurs.execute(qurytext)
    database.commit()
    database.close()