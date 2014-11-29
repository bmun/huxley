/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

require('jquery.cookie');

var $ = require('jquery');
var React = require('react');
var Router = require('react-router');

var CurrentUserStore = require('./huxley/stores/CurrentUserStore');
var Huxley = require('./huxley/Huxley');

var AdvisorAssignmentsView = require('./huxley/components/AdvisorAssignmentsView');
var AdvisorProfileView = require('./huxley/components/AdvisorProfileView');
var ForgotPasswordView = require('./huxley/components/ForgotPasswordView');
var LoginView = require('./huxley/components/LoginView');
var NotFoundView = require('./huxley/components/NotFoundView');
var PasswordResetSuccessView = require('./huxley/components/PasswordResetSuccessView');
var RedirectView = require('./huxley/components/RedirectView');
// var RegistrationView = require('./huxley/components/RegistrationView');
var RegistrationClosedView = require('./huxley/components/RegistrationClosedView');
var RegistrationSuccessView = require('./huxley/components/RegistrationSuccessView');
var RegistrationWaitlistView = require('./huxley/components/RegistrationWaitlistView');

var DefaultRoute = Router.DefaultRoute;
var NotFoundRoute = Router.NotFoundRoute;
var Routes = Router.Routes;
var Route = Router.Route;

var routes = (
  <Route path="/" handler={Huxley}>
    <Route path="/login" handler={LoginView} />
    <Route path="/password" handler={ForgotPasswordView} />
    <Route path="/password/reset" handler={PasswordResetSuccessView} />
    <Route path="/register" handler={RegistrationClosedView} />
    <Route path="/register/success" handler={RegistrationSuccessView} />
    <Route path="/register/waitlist" handler={RegistrationWaitlistView} />
    <Route path="/advisor/profile" handler={AdvisorProfileView} />
    <Route path="/advisor/assignments" handler={AdvisorAssignmentsView} />
    <DefaultRoute handler={RedirectView} />
    <NotFoundRoute handler={NotFoundView} />
  </Route>
);

$(function() {
  Router.run(routes, function(Handler) {
    React.render(
      <Handler />,
      document.getElementById('huxley-app')
    );
  });
});

CurrentUserStore.bootstrap();

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
      // TODO: check that it's same origin.
      xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
    }
  }
});
