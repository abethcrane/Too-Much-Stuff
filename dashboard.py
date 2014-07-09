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
    print "Content-type: text/html; charset=utf-8"
    print
    template_dir=os.path.join(os.path.dirname(__file__),"templates")
    env=Environment(loader=FileSystemLoader(template_dir),autoescape=True)
    template = env.get_template('default.html')
    
    cur_dir = os.path.dirname(__file__)
    con = sqlite3.connect(os.path.join(cur_dir, "test.db"))
    with con:
        db = con.cursor()
        user_id = get_user_id(db)
        print user_id
        if user_id is not None:
            print template.render(title="Library", cat_unique="", categories=["Book", "DVD"], form_action="/add_item.py", form_name="addItem", items=return_items(db, user_id))
        else:
            print "session cookie not set!"

if __name__ == "__main__":
    main()
