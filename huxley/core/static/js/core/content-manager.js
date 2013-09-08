var ContentManager = {
    init: function() {
        $(document).on('click', 'a.js-nav', function() {
            History.pushState({}, $(this).text(), $(this).attr('href'));
            return false;
        });
    
        History.Adapter.bind(
            window,
            'statechange',
            ContentManager.onStateChange
        );

        // Trigger initial app state.
        window.location.pathname == '/'
            ? History.pushState({}, '', $('html').data('default-path'))
            : History.Adapter.trigger(window, 'statechange');
    },

    // Handles content manipulation on state change.
    onStateChange: function() {
        var state = History.getState();
        var $app = $('#app');
        var initialLoad = $app.is(':hidden');

        $('#appnavbar a.js-nav.currentpage').removeClass('currentpage');
        $('#appnavbar a[href="' + window.location.pathname + '"]')
            .addClass('currentpage');

        if (initialLoad) {
            $app.delay(100).fadeIn(500, function() {
                $('#headerwrapper').slideDown(350, function() {
                    $('#header').slideDown(350);
                });
            });
            
            // Don't load new content if there's already content present.
            if ($('#capsule').is(':parent')) {
                return;
            }
        }

        ContentManager.loadNewContent(state.url, null, initialLoad);
    },

    // Loads new content into the application content container.
    loadNewContent: function(path, data, skipFadeout) {
        var $content = $('.content');
        var $contentwrapper = $('#contentwrapper');

        var fadeoutPromise = $.Deferred(function(deferred) {
            $content.css('height', $content.height() + 'px');
            if (skipFadeout) {
                $contentwrapper.hide();
                $content.addClass('loading');
                deferred.resolve();
            } else {
                $contentwrapper.fadeOut(150, function() {
                    $content.addClass('loading');
                    deferred.resolve();
                });
            }
        }).promise();

        var fetchPromise = $.ajax({
            type: data ? 'POST' : 'GET',
            url: path,
            data: data
        }).promise();

        $.when(fetchPromise, fadeoutPromise)
            .done(function(responseData) {
                var markup = responseData[0];
                $('title').html(markup.match(/<title>(.*?)<\/title>/)[1]);
                $('#capsule').replaceWith($('#capsule', $(markup)));

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
