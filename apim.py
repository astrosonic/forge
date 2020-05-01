from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from libraries import libr_makeacnt, libr_entrydir, libr_fgconfig, libr_makemail
from libraries import libr_inbxpage, libr_trashcan, libr_contacts, libr_grupdata
from libraries import libr_gpmkmail

versinfo = libr_fgconfig.versinfo
erorlist = libr_fgconfig.erorlist

main = Flask(__name__)
main.secret_key = "t0xic0der"

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