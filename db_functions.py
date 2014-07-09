#!/usr/bin/python

import Cookie
import os
import sqlite3

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
    items = []
    for i in item_IDs:
        items.append(query_db(db, "select * from Items where Item_ID=?", args=(i['Item_ID'],), one=True))
    return items


def get_user_id(db):
    try:
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        #print "session = " + cookie["session"].value
        result = query_db(db, "Select User_ID from Sessions where Session_Id=?", (cookie["session"].value,), one=True)
        if result is not None:
            user_id = result["User_ID"]
        else:
            user_id = None
    except (Cookie.CookieError, KeyError):
        user_id = None

    return user_id