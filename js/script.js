$(document).ready( function() {

    // If Android exists then we're on the mobile app, in which case we use touch
    if (window.Android) {
        window.onMobile = true;
    // If it doesn't then we set up a mock android (to remove errors if its called)
    } else {
        window.Android = new MockAndroid();
    }
    
    // Activates the alert space
    $(".alert").alert();

    // Activates all buttons
    $('.btn').button();
    

    // Add the actions; but on mobile we use touchend for user friendliness
    if (window.onMobile) {
    	action = 'touchend';
    } else {
    	action = 'click';
    }

	$('#add-item').on(action, function () {addItem($('#string').val());});
	$('.friend').on(action, function () {addFriend($(this).attr('id'));});
	$('.delete').on(action, function () {deleteItem($(this).attr('id'));});
	$('#scan_button').on(action, function () {
		Android.scanSomething();
	});
	
    // Parse the ISBN String before allowing users to search with it
    // Updates as users type, or click out of the textbox
    $("#string").bind('blur keyup change', function(){
        var newISBN = sanitiseISBN($('#string').val());
        $('#string').text(newISBN);
        errorCode = validISBN(newISBN);
        if (errorCode == "Valid ISBN") {
            $("#unique-help").removeClass("text-danger").addClass("text-success");
            $("#unique-help").text(errorCode);
            $("#add-item").removeClass("disabled");
        } else{
            $("#unique-help").removeClass("text-success").addClass("text-danger");
            $('#unique-help').text(errorCode);
            $('#add-item').addClass("disabled");
        }
    });
    
});


function handleScannedISBN(ISBN) {
    $('#string').text(ISBN);
    $('#add-item').click();
}

// Appends an error message to the page
function throwError(errorMessage) {
    if (errorMessage != "") {
        errorMessage = " : "+errorMessage;
    }
    $("#alertSpace").append("<div class='alert alert-danger'>\
        <button type='button' class='close' data-dismiss='alert'>x</button>\
        <strong>Error!</strong> Could not scan book"+errorMessage+"\
        </strong\
    </div>"); 
}

// Strips all non-digits out
function sanitiseISBN(isbn) {
    return isbn.replace(/[^0-9]/g, ''); 
}

// Checks if the ISBN is a valid length
function validISBN(isbn) {
    if (isbn.length < 9) {
        return "Invalid; Too short";
    } else if (isbn.length > 13) {
        return "Invalid; Too long";
    } else {
        return "Valid ISBN";
    }
    
}

// Clears the text field and sets the button to searching whilst it submits the form
function addItem(id) {
    $.post("add_item.py", {id: id}, function() {
        location.reload();
    });
    $('#add-item').button('loading')
    setTimeout(function () {
      $('#add-item').button('reset')
    }, 3000);
}

function deleteItem(id) {
    $.post("delete_item.py", {id: id}, function() {
        location.reload();
    });
}

function addFriend(id) {
    $.post("add_friend.py", {id: id}, function() {
        location.replace('/dashboard.py?friend_id='+id);
    });
}

// Checks if the ISBN exists
function checkValid(data) {
    if (data["totalItems"] == 0) {
        return false;
    } else {
        return true;
    }
}
