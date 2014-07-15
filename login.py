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

def main():
    print "Content-Type: text/html"
    print """
<head>
    <script src="js/jquery-latest.js"></script>
    <script src="js/fbsdk.js"></script>
    <script src="js/fbsdk_login.js"></script>
</head>
<body>
    <fb:login-button scope="public_profile,email,user_friends" onlogin="checkLoginState();">
    </fb:login-button>
</body>"""

    try:
        # Read the user id from the cookie we set at login
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        print cookie

    except (Cookie.CookieError, KeyError):
        print "argh no cookies"

if __name__ == "__main__":
    main()
