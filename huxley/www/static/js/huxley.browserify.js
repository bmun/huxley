/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

require('jquery.cookie');

var $ = require('jquery');
var React = require('react');
var RRouter = require('rrouter');

var CurrentUserStore = require('./huxley/stores/CurrentUserStore');
var Huxley = require('./huxley/Huxley');

var AdvisorProfileView = require('./huxley/components/AdvisorProfileView');
var ForgotPasswordView = require('./huxley/components/ForgotPasswordView');
var LoginView = require('./huxley/components/LoginView');
var PasswordResetSuccessView = require('./huxley/components/PasswordResetSuccessView');
var RedirectView = require('./huxley/components/RedirectView');
// var RegistrationView = require('./huxley/components/RegistrationView');
var RegistrationClosedView = require('./huxley/components/RegistrationClosedView');
var RegistrationSuccessView = require('./huxley/components/RegistrationSuccessView');
var RegistrationWaitlistView = require('./huxley/components/RegistrationWaitlistView');

var Routes = RRouter.Routes;
var Route = RRouter.Route;

var routes = (
  <Routes>
    <Route path="/" view={RedirectView} />
    <Route path="/login" view={LoginView} />
    <Route path="/password" view={ForgotPasswordView} />
    <Route path="/password/reset" view={PasswordResetSuccessView} />
    <Route path="/register" view={RegistrationClosedView} />
    <Route path="/register/success" view={RegistrationSuccessView} />
    <Route path="/register/waitlist" view={RegistrationWaitlistView} />
    <Route path="/advisor/profile" view={AdvisorProfileView} />

  </Routes>
);

$(function() {
  RRouter.start(routes, function(view) {
    React.renderComponent(
      <Huxley view={view} />,
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
