var ContentManager = {
    
    advisorManagers: [],
    chairManagers: [],
    
    // Initializer function.
    init: function() {
        History.Adapter.bind(window, 'statechange', function(){
            var state = History.getState();
            var handler = $("#app").is(":hidden")
                ? ContentManager.loadInitContent
                : ContentManager.loadNewContent;
            handler(state.url);
        });
        
        $(document).on("click", "a.nav", function() {
            History.pushState({}, $(this).text(), $(this).attr("href"));
            return false;
        });
        
        $(document).on("click", "#appnavbar a.nav", function() {
            $("#appnavbar a.nav.currentpage").removeClass('currentpage');
            $(this).addClass('currentpage');
        });
    
        ContentManager.onPageLoad();
    },
    
    // Fades the initial content into view.
    onPageLoad: function() {
        if(window.location.pathname == '/') {
            History.pushState({}, "", $("html").data("default-path")); 
        } else {
            $(window).trigger('statechange');
        }
    },
    
    // Loads initial content into the application content container.
    loadInitContent: function(path, data) {
        ContentManager.initializeManagers();
        if ($("#splash").is(":visible")) {
            $.ajax({
                url: path,
                success: function(response) {
                    // Replace the title and content.
                    $("title").html(response.match(/<title>(.*?)<\/title>/)[1]);
                    $("#capsule").replaceWith($("#capsule", $(response)));
                    $("#appnavbar a[href='" + window.location.pathname + "']")
                      .addClass('currentpage');
                    // Fade in.
                    $("#splash").delay(250).fadeOut(250, function() {
                        $("#app").delay(250).fadeIn(500, function() {
                            $("#headerwrapper").slideDown(350, function() {
                                $("#header").slideDown(350);
                            });
                        });
                    });
                },
                error: Error.show
            });
        } else {
            $.ajax({
                url: path, 
                success: function(response) {
                  // Replace the title and content.
                  $("title").html(response.match(/<title>(.*?)<\/title>/)[1]);
                  $("#capsule").replaceWith($("#capsule", $(response)));
                  // Fade in.
                  $("#app").delay(250).fadeIn(500);
                },
                error: Error.show
            });
        }
    },
    
    // Loads new content into the application content container.
    loadNewContent: function(path, data) {
        $(".content").css('height', $(".content").height() + "px");
        $(".content #contentwrapper").fadeOut(150, function() {
            $(".content").addClass("loading");
            var method = data ? "POST" : "GET";
            $.ajax({
                type: method,
                url: path,
                data: data,
                success: function(data) {
                    // Replace the title and content.
                    $("title").html(data.match(/<title>(.*?)<\/title>/)[1]);
                    $("#capsule").replaceWith($("#capsule", $(data)));
                    // Animate and fade in.
                    $("#contentwrapper").css({
                        'visibility':'hidden',
                        'display': 'block'
                    });
                    var height = $("#contentwrapper").height();
                    $("#contentwrapper").css({
                        'visibility':'',
                        'display': 'none'
                    });
                    $(".content").animate({height: height}, 500, function() {
                        $(".content").removeClass("loading");
                        $("#contentwrapper").fadeIn(150, function() {
                            $(".content").css('height','');
                        });
                    });
                },
                error: Error.show
            });
        });
    },
    
    // Prepares the UI upon login/logout.
    onLoginLogout: function(redirect, fadetime) {
        $("#container").fadeOut(150, function() {
            $("#container").load(redirect + " #appcontainer", null, function() {
                $("#container").fadeIn(fadetime, function() {
                    History.pushState({}, "", redirect);
                });
            });
        });
    },
    
    // Initializes all the managers in the advisorManagers array.
    initializeManagers: function() {
        var managers;
        type = $("span.usertype span").attr("usertype");
        
        if (type == "advisor") {
            managers = ContentManager.advisorManagers;
        } else if (type == "chair") {
            managers = ContentManager.chairManagers;
        } else {
            managers = [];
        }
        
        for (var i = 0; i < managers.length; i++) {
            managers[i].init();
        }
    }
};

$(function() {
    ContentManager.init();
});
