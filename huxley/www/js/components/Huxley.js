/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var React = require("react");
var ReactRouter = require("react-router");
=======
import React from "react";
import PropTypes from "react-router";
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e

var AdvisorView = require("components/AdvisorView");
var ChairView = require("components/ChairView");
var DelegateView = require("components/DelegateView");
var ConferenceContext = require("components/ConferenceContext");
var CurrentUserStore = require("stores/CurrentUserStore");
var Shaker = require("components/Shaker");
var SupportLink = require("components/SupportLink");
var User = require("utils/User");

require("css/base.less");
require("css/Banner.less");
require("css/JSWarning.less");
require("css/IEWarning.less");

<<<<<<< HEAD
var Huxley = React.createClass({
  mixins: [ReactRouter.History],

  childContextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getChildContext: function () {
=======
class Huxley extends React.Component {
  getChildContext() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    var conference = global.conference;
    return {
      conference: conference,
    };
  }

<<<<<<< HEAD
  componentWillMount: function () {
    CurrentUserStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      if (User.isAnonymous(user)) {
        this.history.pushState(null, "/login");
      } else if (User.isAdvisor(user)) {
        this.history.pushState(null, "/advisor/profile");
      } else if (User.isChair(user)) {
        this.history.pushState(null, "/chair/attendance");
      } else if (User.isDelegate(user)) {
        this.history.pushState(null, "/delegate/profile");
=======
  componentWillMount() {
    CurrentUserStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      if (User.isAnonymous(user)) {
        this.context.history.pushState(null, "/login");
      } else if (User.isAdvisor(user)) {
        this.context.history.pushState(null, "/advisor/profile");
      } else if (User.isChair(user)) {
        this.context.history.pushState(null, "/chair/attendance");
      } else if (User.isDelegate(user)) {
        this.context.history.pushState(null, "/delegate/profile");
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
      }
    });
  }

<<<<<<< HEAD
  render: function () {
=======
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    var user = CurrentUserStore.getCurrentUser();
    if (User.isAnonymous(user)) {
      return (
        <div>
          <Shaker>
            {React.cloneElement(this.props.children, { user: user })}
          </Shaker>
          <SupportLink />
        </div>
      );
    } else if (User.isAdvisor(user)) {
      return (
        <div>
          <AdvisorView user={user}>
            {React.cloneElement(this.props.children, { user: user })}
          </AdvisorView>
          <SupportLink />
        </div>
      );
    } else if (User.isChair(user)) {
      return (
        <div>
          <ChairView user={user}>
            {React.cloneElement(this.props.children, { user: user })}
          </ChairView>
          <SupportLink />
        </div>
      );
    } else if (User.isDelegate(user)) {
      return (
        <div>
          <DelegateView user={user}>
            {React.cloneElement(this.props.children, { user: user })}
          </DelegateView>
          <SupportLink />
        </div>
      );
    }
  }
}

Huxley.childContextTypes = {
  conference: React.PropTypes.shape(ConferenceContext),
};

Huxley.contextTypes = {
  history: PropTypes.history,
};

module.exports = Huxley;
