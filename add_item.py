#!/usr/bin/python

import cgi
import cgitb
import Cookie
import json
import sqlite3
import urllib2
cgitb.enable()

from db_functions import *
from item import *

def add_item(db, item_category, item_unique, user_id):

    cat_uniques = {"Book": "ISBN", "DVD": "ISBN"}

    # Check if item already exists in items table
    item = Item.generic_item(db, item_unique, item_category, cat_uniques[item_category])
    item_ID = item.get_db_id()
    does_own = None

    # If It doesn't exist in the database yet
    if item_ID is None:
        if item_category == "Book":
            item = Book(item_unique)
            item.insert()
        else:
            item.insert()
        item_ID = item.get_db_id()
    else:
        # Check the user doesn't already own this, if they do skip adding it
        does_own = query_db(db, "Select * from Owners where User_ID=? and Item_ID=?", (user_id, item_exists["Item_ID"]), one=True)

    if does_own is None:
        # Add the entry into users
        if item_ID is not None:
            effect_db(db, "Insert into Owners(User_ID, Item_ID) Values (?, ?)", (user_id, item_id))
        #TODO: else?


def main():
   # Get the params
   # Add the user item thing
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
            add_item(db, "Book", item_id, user_id) #Use book as the default item category
            print "Status: 303 Redirect"
            print "Location: dashboard.py"
            print
        else:
            print
            print "Error, not all fields set"
            print "user_id: {0}, item_id: {1}".format(user_id, item_id)
            print form

if __name__ == "__main__":
    main()
