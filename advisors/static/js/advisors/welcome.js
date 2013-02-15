var WelcomeManager = {

    // Initialization function.
    init: function() {
        $(document).on("change", ".content .field input", function() {
            WelcomeManager.setUnsaved();
        });
        
        $(document).on("submit", ".content #welcomepage", WelcomeManager.submit);
    },

    // Sets the SAVE button to saved (green).
    setSaved: function() {
        $(".tablemenu input[type=submit]")
            .removeClass('unsaved')
            .addClass('saved');
    },

    // Sets the SAVE button to unsaved (yellow).
    setUnsaved: function() {
        $(".tablemenu input[type=submit]")
            .removeClass('saved')
            .addClass('unsaved');
    },

    submit: function() {
        // Integer-Only Check
        $.validator.addMethod("IntegersOnly", function(value, element){
            if (this.optional(element)) {
                return /^$/i.test(value) || /^[0-9]+$/i.test(value);
            } else {
                return /^[0-9]+$/i.test(value);
            }
        }, "Please enter a positive number.");
        
        // Zip Code Check
        // Allow 0-9, space, dash
        $.validator.addMethod("zip", function(value, element) {
            if (this.optional(element)) {
                return /^$/i.test(value) || /^[0-9\s\-]+$/i.test(value);
            } else {
                return /^[0-9\s\-]+$/i.test(value);
            }
        }, "Zip codes may only contain numbers, spaces, and dashes.");
        
        // U.S. Phone Number Check
        $.validator.addMethod("phoneNum", function(value, element){
            if (this.optional(element)) {
                return /^$/i.test(value) || /^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$/i.test(value);
            }
            else {
                return /^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$/i.test(value);
            }
        }, "Please enter a valid phone number.");
        
        // International Phone Number
        $.validator.addMethod("intPhone", function(value, element) {
            if (this.optional(element)) {
                return /^$/i.test(value) || /^[0-9\-x\s\+\(\)]+$/i.test(value);
            } else {
                return /^[0-9\-x\s\+\(\)]+$/i.test(value);
            }
        }, "Please enter a valid phone number.");
        
        $("#welcomepage").validate();
        
        if ($(this).valid()) {
            var uri = $("#welcomepage").attr("action");
            $.ajax({
                type: 'POST',
                url: uri,
                data: $(this).serializeArray(),
                success: function(name) {
                    WelcomeManager.setSaved();
                    if ($("#header span.advisorfirstname").text() != $("input[name=firstname]").val()) {
                        $("span.advisorfirstname").each(function() {
                            $(this).fadeOut(200, function() {
                                var exclamation = ($(this).closest("li").length > 0) ? "" : "!";
                                $(this).text($("input[name=firstname]").val() + exclamation);
                                $(this).fadeIn(200);
                            });
                        });
                    }
        
                    if($("#header span.advisorlastname").text() != $("input[name=lastname]").val()){
                        $("span.advisorlastname").fadeOut(200, function() {
                            $(this).text($("input[name=lastname]").val());
                            $(this).fadeIn(200);
                        });
                    }
        
                    if($("span.schoolname").text() != $("input[name=schoolname]").val()){
                        $("span.schoolname").fadeOut(200, function() {
                            $(this).text($("input[name=schoolname]").val());
                            $(this).fadeIn(200);
                        });
                    }
                },
            });
        }
        return false;	
    },

    toString: function(){
        return "WelcomeManager";
    }
}

ContentManager.advisorManagers.push(WelcomeManager);

$(function() {

    // TODO: MOVE TO UI ----------------------------------------
    function setGreen(id) {
        $(id).removeClass('negative').addClass('good');
    }
    
    function setRed(id) {
        $(id).removeClass('good').addClass('negative');
    }
});