$(function() {

    // Sets the Save button to 'unsaved'.
    function setUnsaved() {
        $(".tablemenu input[type=submit]")
            .removeClass('saved')
            .addClass('unsaved');
    }

    // Sets the Save button to 'saved'.
    function setSaved() {
        $(".tablemenu input[type=submit]")
            .removeClass('unsaved')
            .addClass('saved');
    }

    // On submission...
    $(document).on("submit", "#form-summaries", function() {
        var uri = $(this).attr("action");

        var data = [];
        $('tr.delegateinfo').each(function() {
            row = {};
            row['id'] = $(this).data('slotId');
            row['textfield'] = $(this).find('td.summary textarea').val();
            row['name'] = $(this).find('td.name').html();
            row['country'] = $(this).find('td.country').html();
            data.push(row);
        });

        var json_data = {
            'delegate_slots' : JSON.stringify(data),
            'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").attr('value')
        };

        $.ajax({
            type: "POST",
            url: "/chair/summaries",
            data: json_data,
            contentType: "application/x-www-form-urlencoded; charset=utf-8",
            success: function(name) {
                setSaved();
            }
        });

        return false;
    });

    // Changes the cursor to pointer upon hover.
    $(document).on("mouseover", "#form-summaries .button", function() {
        $(this).css('cursor', 'pointer');
    });

    // Changes the cursor to the default upon mouseout.
    $(document).on("mouseout", "#form-summaries .button", function() {
        $(this).css('cursor', 'auto');
    });

    // Sets the state to unsaved upon making comments in text fields.
    $(document).on("click", "#form-summaries textarea", function() {
        setUnsaved();
    });
});