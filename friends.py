#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
import cgitb
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
        
        user_id = get_user_id(db)
        display_id = user_id

        if user_id is not None:
            template_dir=os.path.join(os.path.dirname(__file__),"templates")
            env=Environment(loader=FileSystemLoader(template_dir),autoescape=True)
            template = env.get_template('friends_list.html')

            print
            print template.render(title="Friends", headings=["name"], friends=list_friends(db)) #TODO: call to fb to get friendslist
            #TODO: When we click the name to see their list, add them to friends db

        else:
            print "Status: 303 Redirect"
            print "Location: login.py"

if __name__ == "__main__":
    main()
