$(document).ready( function() {
    window.fbAsyncInit = function() {
        FB.init({
            appId        : '1492256340991855',
            cookie        : true,    // enable cookies to allow the server to access the session
            xfbml        : true,    // parse social plugins on this page
            version        : 'v2.0' // use version 2.0
        });

        // If we're on mobile we let the Android side handle logged in stuff
        if (!window.onMobile) {
            // Useful to call it on every page in case someone logs out/in of fb to a different account
            FB.getLoginStatus(function(response) {
                statusChangeCallback(response);
            });
        }
        
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

// This function is called when someone finishes with the Login
// Button.    See the onlogin handler attached to it in the sample code below.
function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}

function setCookies(auth, id, name) {
	// TODO: if auth token changed then reload page
    document.cookie = "access_token="+auth
    document.cookie = "user_id="+id;
    document.cookie = "fb_name="+name;
    // Set the 'hi name' text in case it was blank before
    $('#username').text("Hi "+name+"!");
}
