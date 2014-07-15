/* Class that implements everything the JSI does for the backend
Useful for testing in a browser - this removes errors for 'Android not defined' */
$.Class.extend("MockAndroid", {

    init: function () {
        this.data = '';
    },

    serverSuccess: function (deviceId, name) {
    },

    serverError: function (deviceId, name) {
    },

    getServerUrl: function() {
        return 'localhost';
    },

    getData: function(roomId, capId) {
        return this.data;
    },

    storeData: function(data) {
        this.data = data;
    },

    toast: function(data) {
        alert(data);
    },

    getToken: function() {
        return '';
    }
});
