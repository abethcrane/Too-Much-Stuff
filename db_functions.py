#!/usr/bin/python

import Cookie
import json
import os
import sqlite3
import urllib2

from fb_functions import *

def effect_db(db, action, args=()):
    db.execute(action, args)

def query_db(db, query, args=(), one=False):
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
    if one:
        if rv:
            return rv[0]
        else:
            return None
    else:
        return rv

def return_items(db, user_id, item_type="Books"):
    item_IDs = query_db(db, "select Item_ID from Owners where User_ID=?", args=(user_id,))
    if item_IDs is None:
        return None

    items = []
    for i in item_IDs:
        items.append(query_db(db, "select * from Items where Item_ID=?", args=(i['Item_ID'],), one=True))
    return items
    
def add_user(db, fb_id):
    effect_db(db, "insert into Users(FB_ID) Values(?)", (fb_id,))

def get_user_id(db):
    user_id = None
    auth = None
    app_id = "1492256340991855"
    app_secret = "9c56bc1468a886c8d7fc986f3c3930e3"
    
    # Access token generated from call to below API
    # https://graph.facebook.com/oauth/access_token?client_id={app-id}&client_secret={app-secret}&grant_type=client_credentials
    access_token="1492256340991855|W8gMh9CZ6mXCwTUVipyhYopdRVU"

    try:
        # Read the user id from the cookie we set at login
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])

        if "user_id" in cookie:
            user_id = query_db(db, "select User_ID from Users where FB_ID=?", args=(cookie["user_id"].value,), one=True)

            # This must be a new user, create an entry for them
            if user_id is None:
                add_user(db, data["user_id"])
                user_id = query_db(db, "select User_ID from Users where FB_ID=?", args=(data["user_id"],), one=True)

    except (Cookie.CookieError, KeyError):
        user_id = -1

    return user_id