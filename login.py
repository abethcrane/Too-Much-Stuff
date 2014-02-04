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
<form action="/itemLibrary/login.py" method="post" name="login">
Username<input type="text" name="userid"/>
Password<input type="password" name="pswrd"/>
<input type="submit" onclick="" value="Login"/>
<input type="reset" value="Cancel"/>
</form>"""

def generate_session_id(db):
    check = 1
    # Don't reuse a session ID already in the database
    while check is not None:
        cur_rand = random.randint(0, 1000000000)
        check = query_db(db, "select * from Sessions where Session_ID=?",(cur_rand,), one=True)
    return cur_rand

def make_cookie(db):
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    cookie = Cookie.SimpleCookie()
    cookie["session"] = generate_session_id(db)
    cookie["session"]["domain"] = "ndrewsemler.com"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    return cookie

def store_cookie(db, user_id, cookie):
    effect_db(db, "insert into Sessions Values(?, ?, ?)", (cookie["session"].value, user_id, 1))

def validate_user(db, user, user_pass):
    password = query_db(db, "select Password from Users where Email=?", args=(user,), one=True)
    #print "Password should be", password
    if password is None:
        # Prompt to signup
        return False
    elif password['Password'] == user_pass:
        return True
    else:
        return False

def main():
    
    print "Content-Type: text/html"
    con = sqlite3.connect("/var/www/itemLibrary/test.db")
    with con:
        db = con.cursor()
        form = cgi.FieldStorage()

        user = None
        user_pass = None

        # Get data from fields
        if 'userid' in form:
            user = form.getvalue('userid')
        if 'pswrd' in form:
            user_pass = form.getvalue('pswrd')

        if user is not None and user_pass is not None:
            if validate_user(db, user, user_pass):
                cookie = make_cookie(db)
                user_id = query_db(db, "Select User_ID from Users where Email=?", args=(user,), one=True)
                if user_id is not None:
                    user_id = user_id["User_ID"]
                else:
                    print "That's a weird error"
                store_cookie(db, user_id, cookie)
                print cookie.output()
                print "Status: 303 Redirect"
                print "Location: dashboard.py"
                print
                return
            else:
                print 
                print "Invalid username or password"
                print_login()
        else:
            print
            print_login()
        
        #data = query_db(con, 'SELECT SQLITE_VERSION()', one=True)
        #print "SQLite version: %s" % data  


if __name__ == "__main__":
    main()
