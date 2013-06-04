$(function() {
    $(document).on("click", ".accordion-topic", function() {
        if ($(this).next().is(':hidden')) {
            $(".accordion-topic").removeClass('active');
            $(".accordion-topic").next().children('p').fadeOut(150);
            $(".accordion-topic").next().slideUp(200);
            $(this).next().children('p').fadeIn(150);
            $(this).toggleClass('active').next().slideDown(200);
        } else {
            $(this).next().children('p').fadeOut(150);
            $(this).removeClass('active').next().slideUp(200);
        }
        
        return false;
    });
});