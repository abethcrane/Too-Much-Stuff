#!/usr/bin/python

import cgi
import cgitb
import json
import sqlite3
import urllib2
cgitb.enable()

from db_functions import *

def add_friend(db, user_id, friend_id):
    #TODO: Fix up the fact that users might cease to be friends
    # Don't add them if they're already friends
    if query_db(db, "Select * from Friends where User_ID=? AND Friend_ID=?", args=(user_id, friend_id,), one=True) is None:
        effect_db(db, "Insert into Friends(User_ID, Friend_ID) Values(?,?)", args=(user_id, friend_id,))

def main():
   # Get the params
    print "Content-Type: text/html"

    con = sqlite3.connect("test.db")
    with con:
        db = con.cursor()
        user_id = get_user_id(db)
        form = cgi.FieldStorage()

        friend_id = None
        if "id" in form:
            friend_id = form.getvalue("id")

        if user_id is not None and friend_id is not None:
            add_friend(db, user_id, friend_id)
            print
        else:
            print
            print "Error, not all fields set", form

if __name__ == "__main__":
    main()



