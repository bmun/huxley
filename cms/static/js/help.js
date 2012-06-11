$(function(){    
    // Accordion Stuff
    // Tutorial courtesy of: http://www.sohtanaka.com/web-design/simple-accordion-w-css-and-jquery/
    
    // Initialization
    $(".acc_content").hide(); // Make sure they're all closed
    
    // When clicked...
    
    $(".content").delegate(".acc_topic", "click", function(){
        if ($(this).next().is(':hidden')) {
                $(".acc_topic").removeClass('active');
                $(".acc_topic").next().children('p').fadeOut(150);
                $(".acc_topic").next().slideUp(200);
                $(this).next().children('p').fadeIn(150);
                $(this).toggleClass('active').next().slideDown(200);
        } else {
                $(this).next().children('p').fadeOut(150);
                $(this).removeClass('active').next().slideUp(200);
        }
        return false; // Think this overrides default behavior?
    });
});