#!/usr/bin/python

import cgi
import cgitb
import Cookie
import json
#import requests
import sqlite3
import urllib2
cgitb.enable()

from db_functions import *

cat_uniques = {"Book": "ISBN", "DVD": "ISBN"}

def delete_item(db, user_id, item_id):
    """Unlinks the item and user - doesn't remove the item, as that is expensive with look ups"""
    if item_id is not None:
        effect_db(db, "Delete from Owners where Item_ID=? and User_ID=?", args=(item_id, user_id))     

def main():
   # Get the params
   # Delete the user's requested item
    print "Content-Type: text/html"
    
    con = sqlite3.connect("test.db")
    with con:
        db = con.cursor()
        user_id = get_user_id(db)
        
        form = cgi.FieldStorage()

        item_id = None
        if "id" in form:
            item_id = form.getvalue("id")

        if user_id is not None and item_id is not None:
            delete_item(db, user_id, item_id)
            print
        else:
            print
            print "Error, not all fields set", form

if __name__ == "__main__":
    main()



