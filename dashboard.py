#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
import cgitb
import Cookie
import os
import sqlite3

from db_functions import *
from fb_functions import *
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

        if user_id is not None:
            template_dir=os.path.join(os.path.dirname(__file__),"templates")
            env=Environment(loader=FileSystemLoader(template_dir),autoescape=True)

            search_term = None
            if 'search_term' in form:
                search_term = sanitise_search(form.getvalue('search_term'))

            # Get these from Item class eventually
            attributes = ["Author", "Title"]

            # Set this up; if it's us we have delete, otherwise we'll redo it for our friend
            data = []
            for attr in attributes:
                data.append({"name": attr, "datatype": "string", "editable": "true"})
            data.append({"name":"Delete?", "datatype":"html", "editable":"false"})

            # Assuming we are displaying our own data
            template = env.get_template('own_library.html')
            template_dict = {"name": get_name_from_cookie(), "title" :"My Library", "categories":["Book", "DVD"],
                                     "form_name":"addItem", "attributes":attributes, "items":return_items(db, user_id, search_term), "own":True}

            # If user is specified in url
            if 'friend_id' in form:
                friend_id = form.getvalue('friend_id')

                # And if user is friends with that user (store in db i guess)
                is_friend = query_db(db, "select * from Friends where User_ID=? AND Friend_ID=?", args=(user_id, friend_id,), one=True)
                if is_friend is not None:
                    # Display that user's data
                    friend_name = query_db(db, "select name from Users where User_ID=?", args=(friend_id,), one = True)
                    if friend_name is not None:
                        friend_name = friend_name["name"]
                    else:
                        friend_name = "Your friend"
                    template = env.get_template('item_table.html')
                    template_dict = {"name": get_name_from_cookie(), "title":"{0}'s Library".format(friend_name), "attributes":attributes,
                                             "items":return_items(db, friend_id, search_term), "own":False}

                    data = []
                    for attr in attributes:
                        data.append({"name": attr, "datatype": "string", "editable": "true"})


            print
            print data
            template_dict["data"] = json.dumps(data)
            print template.render(**template_dict)
        else:
            print "Status: 303 Redirect"
            print "Location: login.py"

if __name__ == "__main__":
    main()
