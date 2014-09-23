#!/usr/bin/python

import cgi
import cgitb
import sqlite3
cgitb.enable()

from db_functions import *
from item import *

def update_item(db, item_category, item_unique, column, value, user_id):

    # Find out item in the database
    item = Item.generic_item(item_unique, item_category, cat_uniques[item_category])
    item_ID = item.get_db_id()

    # TODO: Possibly check it already exists in db, but it really should
    # TODO: Possibly make this be a local change not global, but for now YOLO

    # Now modify item in database
    effect_db(db, "Update {0} set {1}='{2}' where Item_ID=?".format(item.table, column, value), (item_ID,))

def main():
   # Get the params
   # Add the user item thing
    print "Content-Type: text/html"
    print
    print "Yay"
    con = sqlite3.connect("test.db")
    with con:
        db = con.cursor()
        user_id = get_user_id(db)
        print user_id
        form = cgi.FieldStorage()

        value = col= item_id = None
        if "id" in form:
            item_id = form.getvalue("id")
        if "column" in form:
            col = form.getvalue("column")
        if "value" in form:
            value = form.getvalue("value")

        print item_id, col, value

        if user_id is not None and item_id is not None and col is not None and value is not None:
            update_item(db, "Book", item_id, col, value, user_id) #Use book as the default item category
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
