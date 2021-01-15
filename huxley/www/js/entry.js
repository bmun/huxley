/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import 'core-js';
import React from "react";
import {BrowserHistory} from "utils/BrowserHistory";
import {Router, Route, Switch} from 'react-router-dom';
var ReactDOM = require('react-dom');

var {CurrentUserActions} = require('actions/CurrentUserActions');
var {Huxley} = require('components/Huxley');
var {AdvisorAssignmentsView} = require('components/AdvisorAssignmentsView');
var {AdvisorFeedbackView} = require('components/AdvisorFeedbackView');
var {AdvisorPaperView} = require('components/AdvisorPaperView');
var {AdvisorProfileView} = require('components/AdvisorProfileView');
var {AdvisorRosterView} = require('components/AdvisorRosterView');
var {ChairAttendanceView} = require('components/ChairAttendanceView');
var {ChairCommitteeFeedbackView} = require('components/ChairCommitteeFeedbackView');
var {ChairDelegateEmailView} = require('components/ChairDelegateEmailView');
var {ChairPapersView} = require('components/ChairPapersView');
var {ChairRubricView} = require('components/ChairRubricView');
var {ChairSummaryView} = require('components/ChairSummaryView');
var {DelegateCommitteeFeedbackView} = require('components/DelegateCommitteeFeedbackView');
var {DelegatePaperView} = require('components/DelegatePaperView');
var {DelegateProfileView} = require('components/DelegateProfileView');
var {ForgotPasswordView} = require('components/ForgotPasswordView');
var {LoginView} = require('components/LoginView');
var {NotFoundView} = require('components/NotFoundView');
var {PasswordResetSuccessView} = require('components/PasswordResetSuccessView');
var {RedirectView} = require('components/RedirectView');
var {RegistrationView} = require('components/RegistrationView');
var {RegistrationClosedView} = require('components/RegistrationClosedView');
var {RegistrationSuccessView} = require('components/RegistrationSuccessView');
var {RegistrationWaitlistView} = require('components/RegistrationWaitlistView');

var routes = (
  <Route path="/" component={Huxley}> 
  <Switch>
    <Route path="/login" component={LoginView} />
    <Route path="/password" component={ForgotPasswordView} />
    <Route path="/password/reset" component={PasswordResetSuccessView} />
    <Route
      path="/register"
      component={
        global.conference.registration_open
          ? RegistrationView
          : RegistrationClosedView
      }
    />
    <Route path="/register/success" component={RegistrationSuccessView} />
    <Route path="/register/waitlist" component={RegistrationWaitlistView} />
    <Route path="/advisor/profile" component={AdvisorProfileView} />
    <Route path="/advisor/assignments" component={AdvisorAssignmentsView} />
    <Route path="/advisor/feedback" component={AdvisorFeedbackView} />
    <Route path="/advisor/roster" component={AdvisorRosterView} />
    <Route path="/advisor/papers" component={AdvisorPaperView} />
    <Route path="/chair/attendance" component={ChairAttendanceView} />
    <Route path="/chair/papers" component={ChairPapersView} />
    <Route path="/chair/rubric" component={ChairRubricView} />
    <Route path="/chair/delegate_emails" component={ChairDelegateEmailView} />
    <Route
      path="/chair/committee_feedback"
      component={ChairCommitteeFeedbackView}
    />
    <Route path="/chair/summary" component={ChairSummaryView} />
    <Route
      path="/delegate/committee_feedback"
      component={DelegateCommitteeFeedbackView}
    />
    <Route path="/delegate/profile" component={DelegateProfileView} />
    <Route path="/delegate/paper" component={DelegatePaperView} />
    <Route exact path="/" component={RedirectView} />
    <Route component={NotFoundView} />
  </Switch>
  </Route>
);

window.addEventListener('DOMContentLoaded', () => {
  ReactDOM.render(
    <Router history={BrowserHistory}>{routes}</Router>,
    document.getElementById('huxley-app'),
  );
});

CurrentUserActions.bootstrap();
