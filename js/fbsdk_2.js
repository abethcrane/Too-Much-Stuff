$(document).ready( function() {
    window.fbAsyncInit = function() {
        FB.init({
            appId        : '1492256340991855',
            cookie        : true,    // enable cookies to allow the server to access the session
            xfbml        : true,    // parse social plugins on this page
            version        : 'v2.0' // use version 2.0
        });

        // If we're on mobile we let the Android side handle logged in stuff
        /*if (!window.onMobile) {
            // Useful to call it on every page in case someone logs out/in of fb to a different account
            FB.getLoginStatus(function(response) {
                statusChangeCallback(response);
            });
        }*/
        
    };

    // Load the SDK asynchronously
    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    $('#logout').on('click', function(event) {
        FB.logout(function (response) {
        location.replace('/login.py');
    });
});

});

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
        document.cookie = "access_token="+response.authResponse.accessToken;
        document.cookie = "user_id="+response.authResponse.userID;
        WelcomeName();
    } else if (response.status === 'not_authorized') {
        // The person is logged into Facebook, but not your app.
        console.log('Please log into this app.');
        location.replace('/login.py');
    } else {
        // The person is not logged into Facebook, so we're not sure if
        // they are logged into this app or not.
        console.log('Please log into Facebook.');
        location.replace('/login.py');
    }
}

// This function is called when someone finishes with the Login
// Button.    See the onlogin handler attached to it in the sample code below.
function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}

function WelcomeName() {
    FB.api('/me', function(response) {
        $('#username').text("Hi "+response.name+"!");
    });
}
