from flask import Flask, render_template, request, redirect, url_for, session
from libraries import libr_makeacnt, libr_entrydir, libr_fgconfig, libr_makemail
from libraries import libr_inbxpage, libr_trashcan, libr_contacts, libr_grupdata
from libraries import libr_gpmkmail

versinfo = libr_fgconfig.versinfo
erorlist = libr_fgconfig.erorlist

main = Flask(__name__)
main.secret_key = "t0xic0der"

@main.route("/makemail/", methods=["GET"])
def makemail():
    if request.method == "GET":
        jsondata = request.get_json()
        sendernm = jsondata["sendernm"]
        receiver = jsondata["receiver"]
        subjtext = jsondata["subjtext"]
        conttext = jsondata["conttext"]
        if libr_makemail.acntexst(receiver) is False:
            retndata = {"notecode": "ACNOEXST"}
        else:
            libr_makemail.sendmail(subjtext, conttext, sendernm, receiver)
            retndata = {"notecode": "MAILSENT"}
        return retndata

@main.route("/folocont/", methods=["GET"])
def folocont(usercont):
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        usercont = jsondata["usercont"]
        libr_contacts.addtocnt(usercont, username)
        retndata = {
            "notecode": "USERFOLD"
        }
        return retndata

@main.route("/unfocont/", methods=["GET"])
def unfocont(usercont):
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        usercont = jsondata["usercont"]
        libr_contacts.delfmcnt(usercont, username)
        retndata = {
            "notecode": "USERUNFO"
        }
        return retndata

@main.route("/rmovmail/", methods=["GET"])
def rmovmail():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        paradrct = jsondata["paradrct"]
        mailiden = jsondata["mailiden"]
        libr_inbxpage.movetrsh(paradrct,mailiden)
        retndata = {
            "notecode": "MSGRMOVD"
        }
        return retndata

@main.route("/purgemsg/", methods=["GET"])
def purgemsg():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        paradrct = jsondata["paradrct"]
        mailiden = jsondata["mailiden"]
        libr_trashcan.purgemsg(paradrct, mailiden)
        retndata = {
            "notecode": "MSGPURGD"
        }
        return retndata

@main.route("/rstrmail/", methods=["GET"])
def rstrmail():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        paradrct = jsondata["paradrct"]
        mailiden = jsondata["mailiden"]
        libr_trashcan.moveinbx(paradrct, mailiden)
        retndata = {
            "notecode": "MSGRSTRD"
        }
        return retndata

@main.route("/inbxpage/", methods=["GET"])
def inbxpage():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        recvdict = libr_inbxpage.fetcrecv(username)
        senddict = libr_inbxpage.fetcsend(username)
        retndata = {
            "notecode": "INBXPAGE",
            "recvmail": recvdict,
            "sentmail": senddict,
        }
        return retndata

@main.route("/contacts/", methods=["GET"])
def contacts():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        contlist = libr_contacts.fetccont(username)
        retndata = {
            "notecode": "CONTACTS",
            "contlist": contlist
        }
        return retndata

@main.route("/trashcan/", methods=["GET"])
def trashcan():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        recvdict = libr_trashcan.fetcrecv(username)
        senddict = libr_trashcan.fetcsend(username)
        retndata = {
            "notecode": "TRASHCAN",
            "recvmail": recvdict,
            "sentmail": senddict,
        }
        return retndata

@main.route("/onegroup/", methods=["GET"])
def onegroup():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        grupiden = jsondata["grupiden"]
        grupdata = libr_grupdata.fetcgrup(grupiden)
        listmail = libr_gpmkmail.fetcmail(grupiden, username)
        retndata = {
            "notecode": "GRUPMAIL",
            "grupdata": grupdata,
            "listmail": listmail,
        }
        return retndata

@main.route("/compgrup/", methods=["GET"])
def compgrup():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        grupiden = jsondata["grupiden"]
        subjtext = jsondata["subjtext"]
        conttext = jsondata["conttext"]
        libr_gpmkmail.sendmail(subjtext, conttext, username, grupiden)
        retndata = {
            "notecode": "MAILSENT"
        }
        return retndata

@main.route("/makegrup/", methods=["GET"])
def makegrup():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        grupname = jsondata["grupname"]
        namelist = jsondata["namelist"]
        if libr_grupdata.grupexst(grupname) is True:
            retndata = {
                "notecode": "GRUPEXST",
            }
        else:
            namelist = namelist + username
            partlist = namelist.split(" ")
            if libr_grupdata.doesexst(partlist) is False:
                retndata = {
                    "notecode": "PARTNOEX",
                }
            else:
                identity = libr_grupdata.savegrup(grupname, partlist, username)
                retndata = {
                    "notecode": "GRUPMADE",
                    "grupiden": identity
                }
        return retndata

@main.route("/grupdata/", methods=["GET"])
def grupdata():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        gruplist = libr_grupdata.listfetc(username)
        retndata = {
            "notecode": "GPLSFETC",
            "gruplist": gruplist,
        }
        return retndata

@main.route("/brodcast/", methods=["GET"])
def brodcast():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        retndata = {
            "notecode": "BRODCAST",
            "username": username,
        }
        return retndata

@main.route("/settings/", methods=["GET"])
def settings():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        retndata = {
            "notecode": "SETTINGS",
            "username": username,
        }
        return retndata

@main.route("/makeacnt/", methods=["GET"])
def makeacnt():
    if request.method == "GET":
        jsondata = request.get_json()
        fullname = jsondata["fullname"]
        username = jsondata["username"]
        password = jsondata["password"]
        emailadr = jsondata["emailadr"]
        if libr_entrydir.acntexst(username) is True:
            retndata = {"notecode": "ALRDYEXT"}
        else:
            pkcsiden = libr_makeacnt.saveuser(fullname,username,password,emailadr)
            retndata = {"notecode": "MADEACNT", "pkcsiden": pkcsiden}
        return retndata

@main.route("/entrydir/", methods=["GET"])
def entrydir():
    if request.method == "GET":
        jsondata = request.get_json()
        username = jsondata["username"]
        password = jsondata["password"]
        if libr_entrydir.acntexst(username) is False:
            retndata = {"notecode": "ACNOEXST"}
        else:
            if libr_entrydir.chekuser(username, password) is True:
                retndata = {"notecode": "LOGINOK"}
            else:
                retndata = {"notecode": "WRNGPSWD"}
        return retndata

if __name__ == "__main__":
    main.run(port=9696, host="0.0.0.0")