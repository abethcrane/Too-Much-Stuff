$(document).ready( function() {

    // Activates the alert space
    $(".alert").alert();

    // Activates all buttons
    $('.btn').button();
    
    // Clears the text field and sets the button to searching whilst it submits the form
    $('#add-item').click(function () {
        var btn = $(this)
        btn.button('loading')
        setTimeout(function () {
          btn.button('reset')
        }, 3000)
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
    
    $('friend').click(function () {
        addFriend($(this).attr('id'));
    });
    
});

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


// Toggles the notification button of the ith book box
function switchNotifications(isbn) {
    if ($('#notifications'+isbn).hasClass('btn-success')) {
        $('#notifications'+isbn).addClass('btn-danger');
        $('#notifications'+isbn).removeClass('btn-success');
        $('#notifications'+isbn).html("<i class='icon-remove icon-white'</i>");
    } else {
        $('#notifications'+isbn).addClass('btn-success');
        $('#notifications'+isbn).removeClass('btn-danger');
        $('#notifications'+isbn).html("<i class='icon-ok icon-white'</i>");
        // If the isbn exists in the hashtable
        if (scannedBooks.hasOwnProperty(isbn)) {
            Android.makeNotifications(scannedBooks[isbn].title);        
        }
    }
}

function deleteItem(id) {
    $.post("delete_item.py", {id: id}, function() {location.reload();});
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
