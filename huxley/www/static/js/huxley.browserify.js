/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Cookie = require('js-cookie');
var React = require('react');
var ReactDOM = require('react-dom')
var ReactRouter = require('react-router');

var CurrentUserActions = require('./huxley/actions/CurrentUserActions');
var Huxley = require('./huxley/components/Huxley');
var AdvisorAssignmentsView = require('./huxley/components/AdvisorAssignmentsView');
var AdvisorProfileView = require('./huxley/components/AdvisorProfileView');
var AdvisorRosterView = require('./huxley/components/AdvisorRosterView')
var ForgotPasswordView = require('./huxley/components/ForgotPasswordView');
var LoginView = require('./huxley/components/LoginView');
var NotFoundView = require('./huxley/components/NotFoundView');
var PasswordResetSuccessView = require('./huxley/components/PasswordResetSuccessView');
var RedirectView = require('./huxley/components/RedirectView');
var RegistrationView = require('./huxley/components/RegistrationView');
var RegistrationClosedView = require('./huxley/components/RegistrationClosedView');
var RegistrationSuccessView = require('./huxley/components/RegistrationSuccessView');
var RegistrationWaitlistView = require('./huxley/components/RegistrationWaitlistView');

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
