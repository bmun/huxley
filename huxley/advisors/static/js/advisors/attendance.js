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
    $(document).on("submit", "#form-attendance", function() {
        var uri = $(this).attr("action");
        
        var data = [];
        $('tr.delegateinfo').each(function() {
            row = {};
            row['id'] = $(this).data('slotId');
            $(this).find('td.session input').each(function() {
                row[$(this).attr('name')] = $(this).attr('checked') == 'checked';
            });
            data.push(row);
        });

        var json_data = {
            'delegate_slots' : JSON.stringify(data),
            'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").attr('value')
        };

        $.ajax({
            type: "POST",
            url: uri,
            data: json_data,
            contentType: "application/x-www-form-urlencoded; charset=utf-8",
            success: function(name) {
                setSaved();
            }
        });

        return false;
    });

    // Changes the cursor to pointer upon hover.
    $(document).on("mouseover", "#form-attendance .button", function() {
        $(this).css('cursor', 'pointer');
    });

    // Changes the cursor to the default upon mouseout.
    $(document).on("mouseout", "#form-attendance .button", function() {
        $(this).css('cursor', 'auto');
    });

    // Sets the state to unsaved upon checking or unchecking boxes.
    $(document).on("change", "#form-attendance input[type=checkbox]", function() {
        setUnsaved();
    });
});