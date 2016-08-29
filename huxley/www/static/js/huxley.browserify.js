/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

require('core-js/es6');

var $ = require('jquery');
var Cookie = require('js-cookie');
var React = require('react');
var ReactDOM = require('react-dom')
var ReactRouter = require('react-router');

var CurrentUserActions = require('actions/CurrentUserActions');
var Huxley = require('components/Huxley');
var AdvisorAssignmentsView = require('components/AdvisorAssignmentsView');
var AdvisorProfileView = require('components/AdvisorProfileView');
var AdvisorRosterView = require('components/AdvisorRosterView');
var ForgotPasswordView = require('components/ForgotPasswordView');
var LoginView = require('components/LoginView');
var NotFoundView = require('components/NotFoundView');
var PasswordResetSuccessView = require('components/PasswordResetSuccessView');
var RedirectView = require('components/RedirectView');
var RegistrationView = require('components/RegistrationView');
var RegistrationClosedView = require('components/RegistrationClosedView');
var RegistrationSuccessView = require('components/RegistrationSuccessView');
var RegistrationWaitlistView = require('components/RegistrationWaitlistView');

var IndexRoute = ReactRouter.IndexRoute;
var Router = ReactRouter.Router;
var Route = ReactRouter.Route;

var routes = (
  <Route path="/" component={Huxley}>
    <Route path="/login" component={LoginView} />
    <Route path="/password" component={ForgotPasswordView} />
    <Route path="/password/reset" component={PasswordResetSuccessView} />
    <Route
      path="/register"
      component={global.conference.registration_open
        ? RegistrationView
        : RegistrationClosedView
      }
    />
    <Route path="/register/success" component={RegistrationSuccessView} />
    <Route path="/register/waitlist" component={RegistrationWaitlistView} />
    <Route path="/advisor/profile" component={AdvisorProfileView} />
    <Route path="/advisor/assignments" component={AdvisorAssignmentsView} />
    <Route path="/advisor/roster" component={AdvisorRosterView} />
    <IndexRoute component={RedirectView} />
    <Route path="*" component={NotFoundView} />
  </Route>
);

$(function() {
  ReactDOM.render(
    <Router>{routes}</Router>,
    document.getElementById('huxley-app')
  );}
);

CurrentUserActions.bootstrap();

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
      // TODO: check that it's same origin.
      xhr.setRequestHeader('X-CSRFToken', Cookie.get('csrftoken'));
    }
  }
});
