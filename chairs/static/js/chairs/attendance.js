$(function() {
	// CSRF Token for AJAX calls
	$(document).ajaxSend(function(event, xhr, settings) {
	    function getCookie(name) {
	        var cookieValue = null;
	        if (document.cookie && document.cookie != '') {
	            var cookies = document.cookie.split(';');
	            for (var i = 0; i < cookies.length; i++) {
	                var cookie = jQuery.trim(cookies[i]);
	                // Does this cookie string begin with the name we want?
	                if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                    break;
	                }
	            }
	        }
	        return cookieValue;
	    }
	    function sameOrigin(url) {
	        // url could be relative or scheme relative or absolute
	        var host = document.location.host; // host + port
	        var protocol = document.location.protocol;
	        var sr_origin = '//' + host;
	        var origin = protocol + sr_origin;
	        // Allow absolute or scheme relative URLs to same origin
	        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	            // or any other URL that isn't scheme relative or absolute i.e relative.
	            !(/^(\/\/|http:|https:).*/.test(url));
	    }
	    function safeMethod(method) {
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }

	    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
	        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	    }
	});

	// Sets the Save button to 'unsaved'.
	function setUnsaved() {
		$("#tablemenu input[type=submit]")
			.removeClass('saved')
			.addClass('unsaved');
	}

	// Sets the Save button to 'saved'.
	function setSaved() {
		$("#tablemenu input[type=submit]")
			.removeClass('unsaved')
			.addClass('saved');
	}

	// On submission...
	$(document).on("submit", "#form-attendance", function() {
		var uri = $(this).attr("action");
		var data = [];

		var delegates = $("#div-attendance").find(".delegateinfo");
		delegates.each(function() {
			var delegateid = $(this).attr("delegateid");
			var sessions = $(this).children(".session");
			var session_data = {};

			sessions.each(function() {
				var session_num = $(this).attr("session");
				var input_field = $(this).children("input");
				session_data[session_num] = $(input_field).attr("checked") == "checked";
			});

			var delegate_data = { "delegateid": delegateid, 
								  "sessions": session_data };
			data.push(delegate_data);
		});

		//var csrf_token = $('input[name="csrfmiddlewaretoken"]').attr("value");

		var json_data = { "delegates": data };

		$.ajax({
			type: "POST",
			url: uri,
			data: JSON.stringify(json_data),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
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