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


def print_login():
   print """
<!DOCTYPE html>
<html>
	<head>
		<title>Facebook Login JavaScript Example</title>
		<meta charset="UTF-8">
	</head>
	<body>
		<script>
		  // This is called with the results from from FB.getLoginStatus().
		  function statusChangeCallback(response) {
			console.log('statusChangeCallback');
			console.log(response);
			// The response object is returned with a status field that lets the
			// app know the current login status of the person.
			// Full docs on the response object can be found in the documentation
			// for FB.getLoginStatus().
			if (response.status === 'connected') {
			  // Logged into your app and Facebook.
			  testAPI();
			} else if (response.status === 'not_authorized') {
			  // The person is logged into Facebook, but not your app.
			  document.getElementById('status').innerHTML = 'Please log ' +
				'into this app.';
			} else {
			  // The person is not logged into Facebook, so we're not sure if
			  // they are logged into this app or not.
			  document.getElementById('status').innerHTML = 'Please log ' +
				'into Facebook.';
			}
		  }

		  // This function is called when someone finishes with the Login
		  // Button.  See the onlogin handler attached to it in the sample
		  // code below.
		  function checkLoginState() {
			FB.getLoginStatus(function(response) {
			  statusChangeCallback(response);
			});
		  }

		  window.fbAsyncInit = function() {
		  FB.init({
			appId      : '{your-app-id}',
			cookie     : true,  // enable cookies to allow the server to access 
								// the session
			xfbml      : true,  // parse social plugins on this page
			version    : 'v2.0' // use version 2.0
		  });

		  // Now that we've initialized the JavaScript SDK, we call 
		  // FB.getLoginStatus().  This function gets the state of the
		  // person visiting this page and can return one of three states to
		  // the callback you provide.  They can be:
		  //
		  // 1. Logged into your app ('connected')
		  // 2. Logged into Facebook, but not your app ('not_authorized')
		  // 3. Not logged into Facebook and can't tell if they are logged into
		  //    your app or not.
		  //
		  // These three cases are handled in the callback function.

		  FB.getLoginStatus(function(response) {
			statusChangeCallback(response);
		  });

		  };

		  // Load the SDK asynchronously
		  (function(d, s, id) {
			var js, fjs = d.getElementsByTagName(s)[0];
			if (d.getElementById(id)) return;
			js = d.createElement(s); js.id = id;
			js.src = "//connect.facebook.net/en_US/sdk.js";
			fjs.parentNode.insertBefore(js, fjs);
		  }(document, 'script', 'facebook-jssdk'));

		  // Here we run a very simple test of the Graph API after login is
		  // successful.  See statusChangeCallback() for when this call is made.
		  function testAPI() {
			console.log('Welcome!  Fetching your information.... ');
			FB.api('/me', function(response) {
			  console.log('Successful login for: ' + response.name);
			  document.getElementById('status').innerHTML =
				'Thanks for logging in, ' + response.name + '!';
			});
		  }
		</script>

		<!--
		  Below we include the Login Button social plugin. This button uses
		  the JavaScript SDK to present a graphical Login button that triggers
		  the FB.login() function when clicked.
		-->

		<fb:login-button scope="public_profile,email" onlogin="checkLoginState();">
		</fb:login-button>

		<div id="status">
		</div>
		<form action="/itemLibrary/login.py" method="post" name="login">
			Username!<input type="text" name="userid"/>
			Password!<input type="password" name="pswrd"/>
			<input type="submit" onclick="" value="Login"/>
			<input type="reset" value="Cancel"/>
		</form>
	</body>
</html>
"""

def generate_session_id(db):
    check = 1
    # Don't reuse a session ID already in the database
    while check is not None:
        cur_rand = random.randint(0, 1000000000)
        check = query_db(db, "select * from Sessions where Session_ID=?",(cur_rand,), one=True)
    return cur_rand

def make_cookie(db):
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    cookie = Cookie.SimpleCookie()
    cookie["session"] = generate_session_id(db)
    cookie["session"]["domain"] = "toomuchstuff.bethanycrane.com"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    return cookie

def store_cookie(db, user_id, cookie):
    effect_db(db, "insert into Sessions Values(?, ?, ?)", (cookie["session"].value, user_id, 1))

def validate_user(db, user, user_pass):
    password = query_db(db, "select Password from Users where Email=?", args=(user,), one=True)
    #print "Password should be", password
    if password is None:
        # Prompt to signup
        return False
    elif password['Password'] == user_pass:
        return True
    else:
        return False

def main():
    
    print "Content-Type: text/html"
    con = sqlite3.connect("/home/bethcrane/toomuchstuff.bethanycrane.com/test.db")
    with con:
        db = con.cursor()
        form = cgi.FieldStorage()

        user = None
        user_pass = None

        # Get data from fields
        if 'userid' in form:
            user = form.getvalue('userid')
        if 'pswrd' in form:
            user_pass = form.getvalue('pswrd')

        if user is not None and user_pass is not None:
            if validate_user(db, user, user_pass):
                cookie = make_cookie(db)
                user_id = query_db(db, "Select User_ID from Users where Email=?", args=(user,), one=True)
                if user_id is not None:
                    user_id = user_id["User_ID"]
                else:
                    print "That's a weird error"
                store_cookie(db, user_id, cookie)
                print cookie.output()
                print "Status: 303 Redirect"
                print "Location: dashboard.py"
                print
                return
            else:
                print 
                print "Invalid username or password"
                print_login()
        else:
            print
            print_login()
        
        #data = query_db(con, 'SELECT SQLITE_VERSION()', one=True)
        #print "SQLite version: %s" % data  


if __name__ == "__main__":
    main()
