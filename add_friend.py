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
    if user_id is not None and friend_id is not None:
        effect_db(db, "Insert into Friends(User_ID, Friend_ID) Values(?,?)", args=(user_id, friend_id,))     

def main():
   # Get the params
   # Delete the user's requested item
    print "Content-Type: text/html"
    
    con = sqlite3.connect("test.db")
    with con:
        db = con.cursor()
        user_id = get_user_id(db)
        
        form = cgi.FieldStorage()

        friend_id = None
        if "friend_id" in form:
            friend_id = form.getvalue("friend_id")

        if user_id is not None and friend_id is not None:
            add_friend(db, user_id, friend_id)
            print
        else:
            print
            print "Error, not all fields set", form

if __name__ == "__main__":
    main()



