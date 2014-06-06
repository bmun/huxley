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
var RedirectView = require('./huxley/components/RedirectView');
var RegistrationView = require('./huxley/components/RegistrationView');

var Routes = RRouter.Routes;
var Route = RRouter.Route;

var routes = (
  <Routes>
    <Route name="www" path="/www" view={RedirectView}>
      <Route path="/login" view={LoginView} />
      <Route path="/password" view={ForgotPasswordView} />
      <Route path="/register" view={RegistrationView} />
      <Route path="/advisor/profile" view={AdvisorProfileView} />
    </Route>
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
