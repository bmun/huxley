(function($){
    function loadNewContent(hash, data){
        $(".content").css('height', $(".content").height() + "px");
        $(".content #contentwrapper").fadeOut(150, function(){
                        $(".content #contentwrapper").load(hash + " #capsule", data, function(response, status, xhr){
                                if(status == 'error'){ alert('ERROR! ' + xhr.status + " " + xhr.statusText)};
                                $("#contentwrapper").css({'visibility':'hidden', 'display': 'block'});
                                var height = $("#contentwrapper").height();
                                $("#contentwrapper").css({'visibility':'', 'display': 'none'});
                                $(".content").animate({height: height}, 500, function(){
                                        $("#contentwrapper").fadeIn(150, function(){
                                                $(".content").css('height','');
                                        });
                                });
                        });
                });
    }
    
    function initLoad(hash, data){
        $(".content #contentwrapper").load(hash + " #capsule", data, function(){
                $("#app").delay(250).fadeIn(500);
        });
    }
})(jQuery);