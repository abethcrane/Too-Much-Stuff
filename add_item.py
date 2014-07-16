#!/usr/bin/python

import cgi
import cgitb
import Cookie
import json
import sqlite3
import urllib2
cgitb.enable()

from db_functions import *

cat_uniques = {"Book": "ISBN", "DVD": "ISBN"}

def check_digit(ISBN):
    total = 0
    if len(ISBN) is not 9:
        return ''
    for i in range (0, 9):
        total += (10-i) * int(ISBN[i])
    return str(11 - (total % 11))

def get_ISBN10(ISBN):
    length = len(ISBN)
    if length is 9:
        return ISBN + check_digit(ISBN)
    elif length is 10:
        return ISBN
    elif length is 12 or length is 13:
        ISBN10 = ISBN[3:12]
        return ISBN10 + check_digit(ISBN10)
    else:
        raise TypeError

def lookup_ISBN(ISBN):
    try:
        ISBN10 = get_ISBN10(ISBN)
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn:{0}".format(ISBN10)
        data = json.load(urllib2.urlopen(url))
    except TypeError as e:
        #print "Error; invalid ISBN"
        data = None
    finally:
        return data
    
def get_title(data):
    try:
        title = data["items"][0]["volumeInfo"]["title"]
    except Exception as e:
        title = "Unkown Title"
    finally:
        return title

def get_author(data):
    try:
        author = data["items"][0]["volumeInfo"]["author"]
    except Exception as e:
        try:
            authors = data["items"][0]["volumeInfo"]["authors"]
            author = ""
            for i in authors:
                author = author + i + ", "
            author = author[:-2]
        except Exception as e:
            author = "Unknown Author"
    finally:
        return author

def get_image(data):
    try:
        image = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
    except Exception as e :
        image = "http://placehold.it/140x140"
    finally:
        return image

def get_book_data(ISBN):
    data = lookup_ISBN(ISBN)
    title = get_title(data)
    author = get_author(data)
    image = get_image(data)

    return title, author, image 

def main():
   # Get the params
   # Add the user item thing
    print "Content-Type: text/html"
    
    con = sqlite3.connect("test.db")
    with con:
        db = con.cursor()
        user_id = get_user_id(db)
        
        form = cgi.FieldStorage()

        item_id = None
        if "id" in form:
            item_id = form.getvalue("id")

        if user_id is not None and item_id is not None:
            add_item(db, "Book", item_id, user_id) #Use book as the default item category
            print "Status: 303 Redirect"
            print "Location: dashboard.py"
            print
        else:
            print
            print "Error, not all fields set"
            print "user_id: {0}, item_id: {1}".format(user_id, item_id)
            print form

if __name__ == "__main__":
    main()
