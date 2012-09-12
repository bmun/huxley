function successLabel() {
    return '<label class="success"> Success! </label>';
}

function errorLabel(message) {
    return '<label class="error">' + message + '</label>';
}

$(function() {

    // Opens and closes the Change Password tab.
    $(document).on("click", "#newpassword", function(e) {
        if ($("#changepassword").is(":visible")) {
            $("#changepassword").slideUp(function() {
                $("#changepassword div.input input").val('');
                $("#changepassword #message").hide();
            });
        } else {
            $("#changepassword").slideDown();
        }
        
        return false;
    });

    // Slides the tab up upon clicking on the page.
    $(document).click(function() {
        if ($("#changepassword").is(":visible")) {
            $("#changepassword").slideUp(function() {
                $("#changepassword div.input input").val('');
                $("#changepassword #message").hide();
            });
        }
    });

    // Stops the tab from sliding up when it's clicked on.
    $(document).on("click", ".changepassword", function(e) {
        e.stopPropagation();
    });

    // Submits the changed password to the server and updates UI accordingly.
    $(document).on("submit", "#changepasswordform", function() {
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
                
                $("#changepassword").delay(750).slideUp();
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
            $("#changepassword").effect(
                "shake",
                {direction:"left", times:2, distance:2},
                50
            );
        });
        
        return false;
    });
});