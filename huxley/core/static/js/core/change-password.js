function successLabel() {
    return '<label class="success"> Success! </label>';
}

function errorLabel(message) {
    return '<label class="error">' + message + '</label>';
}

$(function() {

    // Opens and closes the Change Password tab.
    $(document).on("click", "#changepassword-link", function(e) {
        if ($("#changepassword-container").is(":visible")) {
            $("#changepassword-container").slideUp(function() {
                $("#changepassword div.input input").val('');
                $("#changepassword #message").hide();
            });
        } else {
            $("#changepassword-container").slideDown();
        }
        
        return false;
    });

    // Slides the tab up upon clicking on the page.
    $(document).click(function() {
        if ($("#changepassword-container").is(":visible")) {
            $("#changepassword-container").slideUp(function() {
                $("#changepassword div.input input").val('');
                $("#changepassword #message").hide();
            });
        }
    });

    // Stops the tab from sliding up when it's clicked on.
    $(document).on("click", "#changepassword-container", function(e) {
        e.stopPropagation();
    });

    // Submits the changed password to the server and updates UI accordingly.
    $(document).on("submit", "form#changepassword", function() {
        var uri = $(this).attr("action");
        $.post(uri, $(this).serializeArray(), function(data) {
            if (data == 'OK') {
                $("#changepassword input[type=password]").val("");
                if ($("#changepassword #message").is(":visible")) {
                    $("#changepassword #message")
                        .hide()
                        .html(successLabel())
                        .fadeIn(250);
                } else {
                    $("#changepassword #message")
                        .hide()
                        .html(successLabel())
                        .slideDown(250);
                }
                
                $("#changepassword-container").delay(750).slideUp();
                $("#changepassword #message").delay(750).slideUp();
                return false;
            } else if ($("#changepassword #message").is(":visible")) {
                $("#changepassword #message")
                    .hide()
                    .html(errorLabel(data))
                    .fadeIn(250);
            } else {
                $("#changepassword #message")
                    .hide()
                    .html(errorLabel(data))
                    .slideDown(250);
            }
            $("#changepassword-container").effect(
                "shake",
                {direction:"left", times:2, distance:2},
                250
            );
        });
        
        return false;
    });
});