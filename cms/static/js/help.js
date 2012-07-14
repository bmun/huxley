$(function() {

    // Accordion Stuff
    // Tutorial courtesy of:
    // http://www.sohtanaka.com/web-design/simple-accordion-w-css-and-jquery/
    $(document).on("click", ".acc_topic", function(){
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
        
        return false;
    });
});