var ContentManager = {

    // Initializer function.
    init: function() {
        $(document).on('click', 'a.js-nav', function() {
            History.pushState({}, $(this).text(), $(this).attr('href'));
            return false;
        });
        
        $(document).on('click', '#appnavbar a.js-nav', function() {
            $('#appnavbar a.js-nav.currentpage').removeClass('currentpage');
            $(this).addClass('currentpage');
        });

        $(window).on('huxley.contentReady', ContentManager.onContentReady);
    
        History.Adapter.bind(window, 'statechange', function(){
            var state = History.getState();
            var handler = $('#app').is(':hidden')
                ? ContentManager.loadInitialContent
                : ContentManager.loadNewContent;
            handler(state.url);
        });

        // Trigger initial app state.
        window.location.pathname == '/'
            ? History.pushState({}, '', $('html').data('default-path'))
            : History.Adapter.trigger(window, 'statechange');
    },

    // Fades out the splash and fades in the app.
    onContentReady: function() {
        $.Deferred(function(deferred) {
            $splash = $('#splash');
            if ($splash.is(':visible')) {
                $splash.delay(250).fadeOut(250, function() {
                    deferred.resolve();
                });
            } else {
                deferred.resolve();
            }
        }).then(function() {
            $('#app').delay(250).fadeIn(500, function() {
                $('#headerwrapper').slideDown(350, function() {
                    $('#header').slideDown(350);
                });
            });
        });
    },
    
    // Loads initial content into the application content container.
    loadInitialContent: function(path) {
        if(document.getElementById('content-placeholder')) {
            $.get(path, function(data) {
                $('title').html(data.match(/<title>(.*?)<\/title>/)[1]);
                $('#capsule').replaceWith($('#capsule', $(data)));
                $('#appnavbar a[href="' + window.location.pathname + '"]')
                      .addClass('currentpage');
                $(window).trigger('huxley.contentReady');
            });
        } else {
            $(window).trigger('huxley.contentReady');
        }
    },
    
    // Loads new content into the application content container.
    loadNewContent: function(path, data) {
        var $content = $('.content');
        var $contentwrapper = $('#contentwrapper');
        
        var fadeout = $.Deferred(function(deferred) {
            $content.css('height', $content.height() + 'px');
            $contentwrapper.fadeOut(150, function() {
                $content.addClass('loading');
                deferred.resolve();
            });
        });

        var method = data ? 'POST' : 'GET';
        var ajaxCall = $.ajax({type: method, url: path, data: data});

        $.when(ajaxCall, fadeout)
            .done(function(ajaxData) {
                var data = ajaxData[0];
                $('title').html(data.match(/<title>(.*?)<\/title>/)[1]);
                $('#capsule').replaceWith($('#capsule', $(data)));

                $contentwrapper.css({
                    'visibility':'hidden',
                    'display': 'block'
                });
                var height = $contentwrapper.height();
                $contentwrapper.css({
                    'visibility':'',
                    'display': 'none'
                });

                $content.animate({height: height}, 500, function() {
                    $content.removeClass('loading');
                    $contentwrapper.fadeIn(150, function() {
                        $content.css('height','');
                    });
                });
            })
            .fail(Error.show);
    },
    
    // Prepares the UI upon login/logout.
    onLoginLogout: function(redirect, fadetime) {
        var $container = $('#container');
        var fadeout = $.Deferred(function(deferred) {
            $container.fadeOut(150, function() {
                deferred.resolve();
            });
        });

        $.when($.get(redirect), fadeout).done(function(data) {
            $('#appcontainer').replaceWith($('#appcontainer', $(data[0])));
            $container.fadeIn(fadetime, function() {
                History.pushState({}, '', redirect);
            });
        });
    }
};

$(function() {
    ContentManager.init();
});
