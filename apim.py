from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from libraries import libr_makeacnt, libr_entrydir, libr_fgconfig, libr_makemail
from libraries import libr_inbxpage, libr_trashcan, libr_contacts, libr_grupdata
from libraries import libr_gpmkmail

versinfo = libr_fgconfig.versinfo
erorlist = libr_fgconfig.erorlist

main = Flask(__name__)
main.secret_key = "t0xic0der"

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