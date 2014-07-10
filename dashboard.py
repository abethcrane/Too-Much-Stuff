#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
import cgitb
import Cookie
import os
import sqlite3

from db_functions import *
from jinja2 import Template, FileSystemLoader, Environment, PackageLoader

cgitb.enable()

def main():
    print "Content-Type: text/html;"
    
    cur_dir = os.path.dirname(__file__)
    con = sqlite3.connect(os.path.join(cur_dir, "test.db"))
    with con:
        db = con.cursor()
        form = cgi.FieldStorage()
       
        user_id = get_user_id(db)
        display_id = user_id

        if user_id is not None:
            template_dir=os.path.join(os.path.dirname(__file__),"templates")
            env=Environment(loader=FileSystemLoader(template_dir),autoescape=True)
            template = env.get_template('item_table.html')

            # If user is specified in url
            if 'friend_id' in form:
                friend_id = form.getvalue('friend_id')

                # and user is friends with that user (store in db i guess)
                is_friend = query_db(db, "select * from Friends where User_ID=? AND Friend_ID=?", args=(user_id, friend_id,), one=True)
                # display that user's stuff, otherwise our own items
                display_id = friend_id

            print
            print template.render(title="Library", categories=["Book", "DVD"], form_action="/add_item.py", form_name="addItem", attributes=["Author", "Title"], items=return_items(db, display_id))
        else:
            print "Status: 303 Redirect"
            print "Location: login.py"

if __name__ == "__main__":
    main()
