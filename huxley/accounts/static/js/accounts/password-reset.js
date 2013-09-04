$(function() {
    $(document).on('submit', '#password-reset', function() {
        var uri = $(this).attr('action');
        ContentManager.loadNewContent(uri, $(this).serializeArray());
        return false;
    });
});