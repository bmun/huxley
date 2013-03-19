$(function() {

    // Show/hide Country Field based on American/International
    // Change validation rules too
    $(document).on("click", "#content-outer .int_check", function() {
        if ($(this).val() == "international") {
            $(".showhide").slideDown();
            $(".showhide").addClass('required');
            $(".phoneVal").removeClass('phoneNum').addClass('intPhone');
            $("#id_SchoolState").removeClass('required');
        } else {
            $(".showhide").slideUp();
            $(".showhide").removeClass('required');
            $(".phoneVal").removeClass('intPhone').addClass('phoneNum');
            $("#id_SchoolState").addClass('required');
        }
    });

    // Integer-Only Check
    $.validator.addMethod("IntegersOnly", function(value, element) {
        return (this.optional(element))
            ? (/^$/i.test(value) || /^[0-9]+$/i.test(value))
            : /^[0-9]+$/i.test(value);
    }, "Please enter a positive number.");

    // Zip Code Check
    // Allow 0-9, space, dash
    $.validator.addMethod("zip", function(value, element) {
        return (this.optional(element))
            ? (/^$/i.test(value) || /^[0-9\s\-]+$/i.test(value))
            : /^[0-9\s\-]+$/i.test(value);
    }, "Zip codes may only contain numbers, spaces, and dashes.");

    // U.S. Phone Number Check
    $.validator.addMethod("phoneNum", function(value, element){
        if (this.optional(element)) {
            return /^$/i.test(value) || /^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$/i.test(value);
        } else {
            return /^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$/i.test(value);
        }
    }, "Please enter a valid phone number.");

    // International Phone Number
    $.validator.addMethod("intPhone", function(value, element) {
        return (this.optional(element))
            ? (/^$/i.test(value) || /^[0-9\-x\s\+\(\)]+$/i.test(value))
            : /^[0-9\-x\s\+\(\)]+$/i.test(value);
    }, "Please enter a valid phone number.");

    // Username Check
    $.validator.addMethod("username", function(value, element) {
        return this.optional(element) || /^[A-Za-z0-9\_]+$/i.test(value);
    }, "Usernames may only contain letters, numbers, and underscores.");

    // Unique username check.
    $.validator.addMethod("uniqueUser", function(value, element) {
        var unique = false;
        $.ajax({
            type: 'POST',
            async: false,
            url: 'uniqueuser/',
            data: $("#registration").serializeArray(),
            success: function(data, status, jq) {
                unique = (status == "success");
            }
        });
        return unique;
    }, "This username is taken. :(");

    // Password Check.
    $.validator.addMethod("validChars", function(value, element) {
        // Allows `~!@#$%^&*()-_+=? symbols
        return this.optional(element) ||
            /^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$/i.test(value);
    }, "Passwords may only contain letters, numbers, and certain symbols.");

    // Validates the form upon submit and POSTs if it's valid.
    $(document).on("submit", "#content-outer #registration", function() {
        $("#registration").validate({
            messages: {
                FirstName: {required: "Please enter your first name."},
                LastName: {required: "Please enter your last name."},
                Username: {required: "Please enter your desired username."},
                Password: {required: "Please enter a password."},
                Password2: {
                        required: "Please enter a password.",
                        equalTo: "Please enter the same password again."
                },
                SchoolName: {required: "Please enter the name of your school."},
                SchoolAddress: {required: "Please enter the school's address."},
                SchoolCity: {required: "Please enter the city."},
                SchoolState: {required: "Please enter the state."},
                SchoolZip: {required: "Please enter the zip code."},
                SchoolCountry: {required: "Please enter the country."},
                PrimaryName: {required: "Please enter a name."},
                PrimaryEmail: {required: "Please enter an email address."},
                PrimaryPhone: {required: "Please enter a phone number."}
            },

            rules: {
                Username: {
                    minlength:4
                },
                Password: {
                    minlength:6
                },
                Password2: {
                    equalTo:"#id_Password"
                },
                programtype: {
                    minlength:1
                },
                us_or_int: {
                    minlength:1
                }
            }
        });
        
        var uri = $(this).attr("action");
        if($(this).valid()){
            ContentManager.loadNewContent(
                uri,
                $("#registration").serializeArray()
            );
        }
        $('html, body').animate({scrollTop:0}, 'slow');
        return false;
    });
});