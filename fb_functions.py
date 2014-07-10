#!/usr/bin/python

import base64
import Cookie
import json

def parse_signed_request(auth):
    # Auth looks like {postcard}.{payload}
    # e.g. asdlfk2340jasldf.as3492384
    auth = auth.split('.')
    
    # To convert to base64 we have to ensure the padding is correct (multiple of 4)
    lens = len(auth[0])
    lenx = lens - (lens % 4 if lens % 4 else 4)
    postcode = base64.urlsafe_b64decode(auth[0][:lenx])
    lens = len(auth[1])
    lenx = lens - (lens % 4 if lens % 4 else 4)
    payload = base64.urlsafe_b64decode(auth[1][:lenx])
    
    # Because of the padding adjustments, we are missing the last two characters
    payload += "\"}"
    data = json.loads(payload)
    #TODO: Check signatures match
    
    return data
    
def list_friends():
    friends = None
    
    try:
        auth = None
        
        # Read the access token from the fb-set cookie
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        if "access_token" in cookie:
            auth = cookie["access_token"].value
            
        url = "https://graph.facebook.com/me/friends?access_token={0}".format(auth)
        # Use this to translate the oauth code into an oauth token
        response = urllib2.urlopen(url)
        friends = json.load(response)
        print friends
    except (Cookie.CookieError, KeyError):
        friends = None
        
    return friends