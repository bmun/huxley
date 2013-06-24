var Error = {
    _container: null,
    _content: null,
    
    show: function(jqXHR) {
        switch (jqXHR.status) {
            case 403:
                Error.load403();
                break;
            case 404:
                Error.load404();
                break;
            case 500:
                Error.load500();
                break;
            default:
                Error.loadDefault();
                break;
        }
        
        Error._content.modal({
            overlayId: 'error-overlay',
            containerId: 'error-container',
            overlayClose: true,
            onClose: Error.onClose
        });
    },
    
    // Loads a 403 message into the modal.
    load403: function() {
        Error._content.html('Sorry, you don\'t have the authorization to ' +
                            'view this page. If this is a mistake, please ' +
                            'inform us with the Report Bugs tool. Thanks ' +
                            'for your patience, and for using Huxley!');
    },
    
    // Loads a 404 message into the modal.
    load404: function() {
        Error._content.html('Sorry, the page you were looking for does not ' +
                            'exist. Make sure you typed the URL correctly. If ' +
                            'this is an error, please inform us with the Rep' +
                            'ort Bugs tool. Thanks for using Huxley!');
    },
    
    // Loads a 500 message into the modal.
    load500: function() {
        Error._content.html('Sorry, there\'s been some error on our end and we ' +
                            'couldn\'t serve you the page you were looking ' +
                            'for. We\'ve logged the issue and will have it ' +
                            'resolved as soon as possible. Thanks for your ' +
                            'patience, and for using Huxley!');
    },
    
    // Loads a generic message into the modal.
    loadDefault: function() {
        Error._content.html('Sorry, an error occured while processing your ' +
                            'request. We\'ve logged the issue and will have ' +
                            'it resolved as soon as possible. Thanks for ' +
                            'your patience, and for using Huxley!');
    },
    
    onClose: function() {
        Error._container.fadeOut(150, function() {
            $.modal.close();
            if ($(".content").hasClass('content-loading')) {
                History.back();
            } else if ($("#app").is(":hidden")) {
                History.pushState({}, "", $("html").data("default-path"));
            }
        });
    }
}

$(function() {
    Error._container = $("#error-container");
    Error._content = $("#error-content", Error._container);
});