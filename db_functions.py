#!/usr/bin/python

import base64
import Cookie
import json
import os
import sqlite3
import urllib2

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
    user_id = None
    app_id = "1492256340991855"
    app_secret = "9c56bc1468a886c8d7fc986f3c3930e3"
    
    # Access token generated from call to below API
    # https://graph.facebook.com/oauth/access_token?client_id={app-id}&client_secret={app-secret}&grant_type=client_credentials
    access_token="1492256340991855|W8gMh9CZ6mXCwTUVipyhYopdRVU"

    try:
        # Read the auth input token from the fb-set cookie
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        if "fbsr_1492256340991855" in cookie:
            auth = cookie["fbsr_1492256340991855"].value
            
        # We now parse the signed request in order to get the actual oauth token
        auth = auth.split('.')
        lens = len(auth[0])
        lenx = lens - (lens % 4 if lens % 4 else 4)
        postcode = base64.urlsafe_b64decode(auth[0][:lenx])
        lens = len(auth[1])
        lenx = lens - (lens % 4 if lens % 4 else 4)
        payload = base64.urlsafe_b64decode(auth[1][:lenx])
        data = json.load(payload)
        code = data["oauth_token"]
        #TODO: Check signatures match
        
        
        url = "https://graph.facebook.com/oauth/access_token?client_id={0}&redirect_uri=toomuchstuff.bethanycrane.com&client_secret={1}&code={2}".format(app_id, app_secret, code)
        # Use this to translate the token into (amongst other things) a user id
        response = urllib2.urlopen(url)
        data = json.load(response)
        print data
        #auth = data["
        
        
        url = "https://graph.facebook.com/debug_token?input_token={0}&access_token={1}".format(auth, access_token)
        response = urllib2.urlopen(url)
        data = json.load(response)
        print data
    
        # If we were successful, create a new cookie to store the db user id (not fb), that expires at the same time as the other
        # Essentially we are caching here for ease
        if "user_id" in data:
            user_id = query_db(db, "select User_ID from Users where FB_ID=?", args=(data["user_id"]), one=True)

            # This must be a new user, create an entry for them
            if user_id is None:
                add_user(db, data["user_id"])
                user_id = query_db(db, "select User_ID from Users where FB_ID=?", args=(data["user_id"]), one=True)

            user_id_cookie = Cookie.SimpleCookie()
            user_id_cookie["user_ID"] = data["user_id"]
            user_id_cookie["user_ID"]["expires"] = data["expires_at"]

    except (Cookie.CookieError, KeyError):
        user_id = -1

    return user_id
    
def add_user(db, fb_id):
    effect_db(db, "insert into Users(FB_ID) Values(?)", (fb_id))
