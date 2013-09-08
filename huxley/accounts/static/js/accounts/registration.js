$(function() {

    // Show/hide the Country field based on the school's location.
    $(document).on('click', '#registration .international-check', function() {
        if ($(this).val() == 'location/international') {
            $('#id_school_country')
                .attr('disabled', false)
                .attr('value', null)
                .addClass('required');
            $('.phoneVal').removeClass('phoneNum').addClass('intPhone');
            $('#id_school_state').removeClass('required');
        } else {
            $('#id_school_country')
                .attr('disabled', true)
                .attr('value', 'United States of America')
                .removeClass('required');
            $('.phoneVal').removeClass('intPhone').addClass('phoneNum');
            $('#id_school_state').addClass('required');
        }
    });

    // Nonnegative number.
    $.validator.addMethod('positive-integer', function(value, element) {
        return (this.optional(element))
            ? (/^$/i.test(value) || /^[0-9]+$/i.test(value))
            : /^[0-9]+$/i.test(value);
    }, 'Please enter a number.');

    // Zip code: allow 0-9, space, dash
    $.validator.addMethod('zip', function(value, element) {
        return (this.optional(element))
            ? (/^$/i.test(value) || /^[0-9\s\-]+$/i.test(value))
            : /^[0-9\s\-]+$/i.test(value);
    }, 'Zip codes may only contain numbers, spaces, and dashes.');

    // U.S. phone number.
    $.validator.addMethod('phoneNum', function(value, element){
        var PHONE_REGEX =
            /^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$/i;
        if (!PHONE_REGEX.test(value)) {
            return this.optional(element) && /^$/i.test(value);
        }
        return true;
    }, 'Please enter a valid phone number.');

    // International phone number.
    $.validator.addMethod('intPhone', function(value, element) {
        return (this.optional(element))
            ? (/^$/i.test(value) || /^[0-9\-x\s\+\(\)]+$/i.test(value))
            : /^[0-9\-x\s\+\(\)]+$/i.test(value);
    }, 'Please enter a valid phone number.');

    // Username characters.
    $.validator.addMethod('username', function(value, element) {
        return this.optional(element) || /^[A-Za-z0-9\_]+$/i.test(value);
    }, 'Usernames may only contain letters, numbers, and underscores.');

    // Username uniqueness.
    $.validator.addMethod('uniqueUser', function(value, element) {
        var unique = false;
        $.ajax({
            type: 'GET',
            async: false,
            url: 'uniqueuser/',
            data: {'username' : $('#registration input.username').val()},
            success: function(data, status, jq) {
                unique = (status == 'success');
            }
        });
        return unique;
    }, 'We\re sorry, this username is taken.');

    // Password characters.
    $.validator.addMethod('validChars', function(value, element) {
        // Allows `~!@#$%^&*()-_+=? symbols
        return this.optional(element) ||
            /^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$/i.test(value);
    }, 'Passwords may only contain letters, numbers, and certain symbols.');

    // Validates the form upon submit and POSTs if it's valid.
    $(document).on('submit', '#registration', function() {
        $form = $(this);
        $form.validate({
            messages: {
                first_name: {required: 'Please enter your first name.'},
                last_name: {required: 'Please enter your last name.'},
                username: {required: 'Please enter a username.'},
                password: {required: 'Please enter a password.'},
                password2: {
                    required: 'Please enter a password.',
                    equalTo: 'Please enter the same password again.'
                },
                school_name: {required: 'Please enter the school name.'},
                school_address: {required: 'Please enter the school address.'},
                school_city: {required: 'Please enter the city.'},
                school_state: {required: 'Please enter the state.'},
                school_zip: {required: 'Please enter the zip code.'},
                school_country: {required: 'Please enter the country.'},
                primary_name: {required: 'Please enter a name.'},
                primary_email: {required: 'Please enter an email address.'},
                primary_phone: {required: 'Please enter a phone number.'}
            },
            rules: {
                username: {
                    minlength:4
                },
                password: {
                    minlength:6
                },
                password2: {
                    equalTo:'#id_password'
                },
                program_type: {
                    minlength:1
                },
                us_or_int: {
                    minlength:1
                }
            }
        });
        
        var uri = $(this).attr('action');
        if($form.valid()){
            ContentManager.loadNewContent(uri, $form.serializeArray());
        }

        $('html, body').animate({scrollTop:0}, 'slow');
        return false;
    });
});
