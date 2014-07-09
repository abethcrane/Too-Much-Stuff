#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
import cgitb
import Cookie
import datetime
import os
import random
import sqlite3

from db_functions import query_db, effect_db
cgitb.enable()

def print_login():
   print """
<head>
    <script src="js/jquery-latest.js"></script>
    <script src="js/fbsdk.js"></script>
</head>
<body>
    <fb:login-button scope="public_profile,email" onlogin="checkLoginState();">
    </fb:login-button>
    <form name="login_form">
        <input type="hidden" name="authenticated"/>
        <input type="hidden" name="userId"/>
        <input type="hidden" name="expires"/>
    </form>
</body>"""

def generate_session_id(db):
    check = 1
    # Don't reuse a session ID already in the database
    while check is not None:
        cur_rand = random.randint(0, 1000000000)
        check = query_db(db, "select * from Sessions where Session_ID=?",(cur_rand,), one=True)
    return cur_rand

def make_cookie(db, expiration):
    #expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    cookie = Cookie.SimpleCookie()
    cookie["session"] = generate_session_id(db)
    cookie["session"]["domain"] = "toomuchstuff.bethanycrane.com"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expiration
    return cookie

def store_cookie(db, user_id, cookie):
    effect_db(db, "insert into Sessions Values(?, ?, ?)", (cookie["session"].value, user_id, 1))

def main():
    
    print "Content-Type: text/html"
    con = sqlite3.connect("/home/bethcrane/toomuchstuff.bethanycrane.com/test.db")
    with con:
        db = con.cursor()
        
        form = cgi.FieldStorage()
        auth = None
        userId = None
        expires = None
        
        if 'authenticated' in form:
        	auth = form.getvalue('authenticated')
        if 'userId' in form:
        	userId = form.getvalue('userId')
        if 'expires' in form:
        	expires = form.getvalue('expires')
        	
        if auth is "connected":
                cookie = make_cookie(db, expires)
                store_cooke(db, userId, cookie)
                print "Status: 303 Redirect"
                print "Location: dashboard.py"
                print
                return
        else:
            print
            print_login()

if __name__ == "__main__":
    main()
