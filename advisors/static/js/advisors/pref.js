$(function() {	

    // Sets the Save button to unsaved state.
    function setUnsaved(){
        $(".tablemenu input[type=submit]")
            .removeClass('saved')
            .addClass('unsaved');
    }

    // Sets the Save button to saved state.
    function setSaved(){
        $(".tablemenu input[type=submit]")
            .removeClass('unsaved')
            .addClass('saved');
    }

    // Submits the preferences, sets state to saved.
    $(document).on("submit", "#editprefs", function() {
        var uri = $(this).attr("action");
        $.ajax({
            type: 'POST',
            url: uri,
            data: $(this).serializeArray(),
            success: function(name) {
                setSaved();
            }
        });
        return false;
    });

    // Changes the cursor to pointer upon hover.
    $(document).on("mouseover", "#editprefs .button", function() {
        $(this).css('cursor', 'pointer');
    });

    // Changes the cursor to the default upon mouseout.
    $(document).on("mouseout", "#editprefs .button", function() {
        $(this).css('cursor', 'auto');
    });

    // Sets the state to unsaved upon changing an input.
    $(document).on("change", "#editprefs .select", function() {
        setUnsaved();
    });
});