$(document).ready( function() {

    var cat_uniques = {"Book":"ISBN"};

    $("select").change(function () {
        var value = $(this).val();
        //var value = item_category.options[item_category.selectedIndex].value;
        $("#unique-label").text(cat_uniques[value]);
        $('#add_item_2').css("visibility", "visible");
        $('#add_item_2').css("display", "block");
    });

    // Activates the alert space
    $(".alert").alert();

    // Activates all buttons
    $('.btn').button();
    
    // Clears the text field and sets the button to searching whilst it submits the form
    $('#add-item').click(function () {
        //storeBook(blahdata, "9780316228558");            
        //updateISBNTypeahead($('#string').val());
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
            $(".category-unique").removeClass("error").addClass("success");
            $("#unique-help").text(errorCode);
            $("#add-item").removeClass("disabled");
        } else{
            $(".category-unique").removeClass("success").addClass("error");
            $('#unique-help').text(errorCode);
            $('#add-item').addClass("disabled");
        }
    });

    $('.the-icons').bind({
        mouseover: function() {
            $(this).addClass('icon-white');
        },
        mouseout: function() {
            $(this).removeClass('icon-white');
        }
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

// Function called upon scanning/searching for a book
// Either creates a new book, stores it and displays it, or sends an error message
function storeBook(data, isbn) {
    if (checkValid(data) == true) {
            alert(javaBooks.addBook(d).getIsbn10());
            // Add the new book to the hash and order array
            scannedBooks[isbn] = new book(data, isbn);
            scannedBooksOrder.push(isbn);
            // Hide all other boxes and display the new one
            $('.collapse').collapse('hide');
            $('#your-items').prepend(newBox(scannedBooks[isbn], isbn));            
            $('#book'+isbn).collapse('show');             
        $("#alertSpace").html("<div class='alert alert-success'>\
      <button type='button' class='close' data-dismiss='alert'>x</button>\
      <strong>Success!</strong> Scanned <em>"+scannedBooks[isbn].title+"</em>\
      </div>");                         
    } else {
        throwError("");
    }
}



// Checks if the ISBN exists
function checkValid(data) {
    if (data["totalItems"] == 0) {
        return false;
    } else {
        return true;
    }
}
