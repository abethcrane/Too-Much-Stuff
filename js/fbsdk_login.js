// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation for FB.getLoginStatus().
    if (response.status === 'connected') {
        FB.api('/me', function(data) {
            setCookies(response.authResponse.accessToken, response.authResponse.UserID, data.name);
        });
        location.replace('/dashboard.py');
    } else if (response.status === 'not_authorized') {
        // The person is logged into Facebook, but not your app.
        console.log('Please log into this app.');
    } else {
        // The person is not logged into Facebook, so we're not sure if
        // they are logged into this app or not.
        console.log('Please log into Facebook.');
    }
}