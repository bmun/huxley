$(function() {

    // Attempts to log in, and changes the UI accordingly.
    $(document).on("submit", "form#login", function() {
        var credentials = $(this).serializeArray();
        var uri = $(this).attr("action");
        $.post(uri, credentials, function(data) {
            if(data.success === true) {
                ContentManager.onLoginLogout(data.redirect, 250);
            } else {
                $("#errorcontainer")
                    .hide()
                    .html('<label class="error">' + data.error + '</label>')
                    .fadeIn(250);
                $("#app").effect(
                    "shake",
                    {direction:"up", times:2, distance:2},
                    50
                );
            }
        });
        
        return false;
    });

    // Logs out and changes the UI accordingly.
    $(document).on("click", "#logout", function() {
        var uri = $(this).attr("href");
        $.get(uri, function(redirect) {
            $("#header").slideUp(250, function() {
                $("#headerwrapper").slideUp(250, function() {
                    ContentManager.onLoginLogout(redirect, 0);
                });
            });
        });
        
        return false;
    });
});