$(function() {

    // Attempt to log in, and change the UI accordingly.
    $(document).on('submit', 'form#login', function() {
        var credentials = $(this).serializeArray();
        var uri = $(this).attr('action');
        var $loginButton = $(this).find('.login-button');

        $loginButton.addClass('loading');
        $.post(uri, credentials, function(data) {
            if (data.success === true) {
                ContentManager.onLoginLogout(data.redirect);
            } else {
                $loginButton.removeClass('loading');
                $('#errorcontainer')
                    .hide()
                    .html('<label class="error">' + data.error + '</label>')
                    .fadeIn(250);
                $('#app').effect(
                    'shake',
                    {direction: 'up', times: 2, distance: 2},
                    250
                );
            }
        });
        
        return false;
    });

    // Log out and change the UI accordingly.
    $(document).on('click', '#logout', function() {
        var uri = $(this).attr('href');
        $.get(uri, function(redirect) {
            $('#header').slideUp(250, function() {
                $('#headerwrapper').slideUp(250, function() {
                    ContentManager.onLoginLogout(redirect);
                });
            });
        });
        
        return false;
    });
});
