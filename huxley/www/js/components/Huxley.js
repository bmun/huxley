/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import { Route, Switch } from "react-router-dom";
import { history } from "utils/history";

var { AdvisorAssignmentsView } = require("components/AdvisorAssignmentsView");
var { AdvisorFeedbackView } = require("components/AdvisorFeedbackView");
var { AdvisorPaperView } = require("components/AdvisorPaperView");
var { AdvisorProfileView } = require("components/AdvisorProfileView");
var { AdvisorView } = require("components/AdvisorView");
var { AdvisorRosterView } = require("components/AdvisorRosterView");
var { AdvisorZoomLinkView } = require("components/AdvisorZoomLinkView");
var { ChairAttendanceView } = require("components/ChairAttendanceView");
var {
  ChairCommitteeFeedbackView,
} = require("components/ChairCommitteeFeedbackView");
var { ChairDelegateEmailView } = require("components/ChairDelegateEmailView");
var { ChairFeedView } = require("components/ChairFeedView");
var { ChairNoteView } = require("components/ChairNoteView");
var { ChairPapersView } = require("components/ChairPapersView");
var { ChairRubricView } = require("components/ChairRubricView");
var { ChairSummaryView } = require("components/ChairSummaryView");
var { ChairView } = require("components/ChairView");
var { CurrentUserStore } = require("stores/CurrentUserStore");
var {
  DelegateCommitteeFeedbackView,
} = require("components/DelegateCommitteeFeedbackView");
var { DelegatePaperView } = require("components/DelegatePaperView");
var { DelegateProfileView } = require("components/DelegateProfileView");
var { DelegateNoteView } = require("components/DelegateNoteView")
var { DelegateView } = require("components/DelegateView");
var { ForgotPasswordView } = require("components/ForgotPasswordView");
var { LoginView } = require("components/LoginView");
var { NotFoundView } = require("components/NotFoundView");
var {
  PasswordResetSuccessView,
} = require("components/PasswordResetSuccessView");
var { RedirectView } = require("components/RedirectView");
var { RegistrationView } = require("components/RegistrationView");
var { RegistrationClosedView } = require("components/RegistrationClosedView");
var { RegistrationSuccessView } = require("components/RegistrationSuccessView");
var {
  RegistrationWaitlistView,
} = require("components/RegistrationWaitlistView");
var { Shaker } = require("components/Shaker");
var { SupportLink } = require("components/SupportLink");
var { User } = require("utils/User");

require("css/base.less");
require("css/Banner.less");
require("css/JSWarning.less");
require("css/IEWarning.less");

class Huxley extends React.Component {

  componentDidMount() {
    CurrentUserStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      if (User.isAnonymous(user)) {
        history.redirect("/login");
      } else if (User.isAdvisor(user)) {
        history.redirect("/advisor/profile");
      } else if (User.isChair(user)) {
        history.redirect("/chair/attendance");
      } else if (User.isDelegate(user)) {
        history.redirect("/delegate/profile");
      }
    });
  }
  
  render() {
    var user = CurrentUserStore.getCurrentUser();
    if (User.isAnonymous(user)) {
      return (
        <div>
          <Shaker>
            <Switch>
              <Route path="/login">
                <LoginView />
              </Route>
              <Route path="/password">
                <ForgotPasswordView />
              </Route>
              <Route path="/password/reset">
                <PasswordResetSuccessView />
              </Route>
              <Route path="/register/success">
                <RegistrationSuccessView />
              </Route>
              <Route path="/register/waitlist">
                <RegistrationWaitlistView />
              </Route>
              {global.conference.registration_open ? (
                <Route path="/register">
                  <RegistrationView />
                </Route>
              ) : (
                <Route path="/register">
                  <RegistrationClosedView />
                </Route>
              )}
              <Route exact path="/">
                <RedirectView />
              </Route>
              <Route>
                <NotFoundView />
              </Route>
            </Switch>
          </Shaker>
          <SupportLink />
        </div>
      );
    } else if (User.isAdvisor(user)) {
      return (
        <div>
          <AdvisorView user={user}>
            <Switch>
              <Route path="/advisor/profile">
                <AdvisorProfileView />
              </Route>
              <Route path="/advisor/assignments">
                <AdvisorAssignmentsView />
              </Route>
              <Route path="/advisor/feedback">
                <AdvisorFeedbackView />
              </Route>
              <Route path="/advisor/roster">
                <AdvisorRosterView />
              </Route>
              <Route path="/advisor/papers">
                <AdvisorPaperView />
              </Route>
              <Route path="/advisor/zoom-links">
                <AdvisorZoomLinkView />
              </Route>
              <Route exact path="/">
                <RedirectView />
              </Route>
              <Route>
                <NotFoundView />
              </Route>
            </Switch>
          </AdvisorView>
          <SupportLink />
        </div>
      );
    } else if (User.isChair(user)) {
      return (
        <div>
          <ChairView user={user}>
            <Switch>
              <Route path="/chair/attendance">
                <ChairAttendanceView />
              </Route>
              <Route path="/chair/papers">
                <ChairPapersView />
              </Route>
              <Route path="/chair/rubric">
                <ChairRubricView />
              </Route>
              <Route path="/chair/notes">
                <ChairNoteView />
              </Route>
              <Route path="/chair/feed">
                <ChairFeedView />
              </Route>
              <Route path="/chair/delegate_emails">
                <ChairDelegateEmailView />
              </Route>
              <Route path="/chair/committee_feedback">
                <ChairCommitteeFeedbackView />
              </Route>
              <Route path="/chair/summary">
                <ChairSummaryView />
              </Route>
              <Route exact path="/">
                <RedirectView />
              </Route>
              <Route>
                <NotFoundView />
              </Route>
            </Switch>
          </ChairView>
          <SupportLink />
        </div>
      );
    } else if (User.isDelegate(user)) {
      return (
        <div>
          <DelegateView user={user}>
            <Switch>
              <Route path="/delegate/committee_feedback">
                <DelegateCommitteeFeedbackView />
              </Route>
              <Route path="/delegate/profile">
                <DelegateProfileView />
              </Route>
              <Route path="/delegate/paper">
                <DelegatePaperView />
              </Route>
              <Route path="/delegate/notes">
                <DelegateNoteView />
              </Route>
              <Route exact path="/">
                <RedirectView />
              </Route>
              <Route>
                <NotFoundView />
              </Route>
            </Switch>
          </DelegateView>
          <SupportLink />
        </div>
      );
    }
  }
}

export { Huxley };
