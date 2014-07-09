#!/usr/bin/python

import base64

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