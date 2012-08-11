$(function(){
    
    // Phone Number Auto-Formatting
    // Based off of http://nsreekanth.blogspot.com/2010/12/simple-jquery-plugin-to-validate-format.html
    $(document).on("keyup", ".phoneVal", function(k) {
        var userinput = $(this).val();
        var len = userinput.length;
        var currChar = userinput[len-1];
        
        // If it's not an international school, auto-format phone numbers.
        if ($("input:radio[name=us_or_int]:checked").val() != 'international') {
            // If it's not the delete key:
            if (k.which != 8) {
                // Add parentheses around the area code.
                if (userinput.match(/^[0-9]{3}([0-9]{0,3})$/)) {
                    if (len > 3) {
                        $(this).val("(" + userinput.substring(0,3) + ") " + userinput.substring(3));
                    } else {
                        $(this).val("(" + userinput.substring(0,3) + ") ");
                    }
                }
                
                // If user starts with an open paren (and I know people will do it):
                if (userinput.match(/^\([0-9]{3}([0-9]{0,2})$/)) {
                    if (len > 4) {
                        $(this).val(userinput.substring(0,4) + ") " + userinput.substring(4));
                    } else {
                        $(this).val(userinput.substring(0,4) + ") ");
                    }
                }
                
                // Add a dash between xxx and xxxx.
                if (userinput.match(/^\([0-9]{3}\)\s[0-9]{3}([0-9]{0,4})$/)) {
                    if (len > 9) {
                        $(this).val(userinput.substring(0,9) + "-" + userinput.substring(9));
                    } else {
                        $(this).val(userinput.substring(0,9) + "-");
                    }
                }
                
                // Handle phone extensions by adding an 'x'.
                if (userinput.match(/^\([0-9]{3}\)\s[0-9]{3}\-[0-9]{4}[0-9]+$/)) {
                    $(this).val(userinput.substring(0,14) + " x" + userinput.substring(14));
                }
                
                // If there is a space, add the 'x'.
                if (userinput.match(/^\([0-9]{3}\)\s[0-9]{3}\-[0-9]{4}\s$/)) {
                    $(this).val(userinput.substring(0,15) + "x");
                }
                
                if (userinput.match(/^\([0-9]{3}\)\s[0-9]{3}\-[0-9]{4}x([0-9]+)?$/)) {
                    $(this).val(userinput.substring(0,14) + " " + userinput.substring(14));
                }
                
                // Prevent invalid chars (anything but numbers, open parenthesis, dash, space).
                if (len > 0 && !currChar.match(/^[0-9\-\s\(x]$/)) {
                    $(this).val(userinput.substring(0, len-1));
                }
                
                // Just in case the user decides to hold down numbers:
                if (userinput.match(/^[0-9]{10}([0-9]+)?$/)) {
                    $(this).val("(" + userinput.substring(0,3) + ") " + userinput.substring(3,6) + "-" + userinput.substring(6,10));
                }
                
                // If extension exceeds 5 digits, cap to 5 digits.
                if (userinput.match(/^\([0-9]{3}\)\s[0-9]{3}\-[0-9]{4}\sx[0-9]{5}[0-9]+$/)) {
                    $(this).val(userinput.substring(0,21));
                }
            // If it is the delete key:
            } else {
                // Handle deleting ') ' after area code.
                if (len > 0 && (userinput.match(/^\([0-9]{3}$/) || userinput.match(/^\([0-9]{3}\)$/))) {
                    $(this).val(userinput.substring(1,3));
                }
                
                // Handle the dash.
                if (userinput.match(/^\([0-9]{3}\)\s[0-9]{3}$/)) {
                    $(this).val(userinput.substring(0,8));
                }
                
                // Handle extension (deletes whitespace if 'x' is deleted)
                if (userinput.match(/^\([0-9]{3}\)\s[0-9]{3}\-[0-9]{4}\s$/)) {
                    $(this).val(userinput.substring(0,14));
                }
            }	
        }
    });
})