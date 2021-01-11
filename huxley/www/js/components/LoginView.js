/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var cx = require("classnames");
var React = require("react");
var ReactRouter = require("react-router");
=======
import cx from "classnames";
import React from "react";
import PropTypes from "react-router";
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e

var Button = require("components/core/Button");
var ConferenceContext = require("components/ConferenceContext");
var CurrentUserActions = require("actions/CurrentUserActions");
var NavLink = require("components/NavLink");
var OuterView = require("components/OuterView");
var ServerAPI = require("lib/ServerAPI");
var StatusLabel = require("components/core/StatusLabel");
var TextInput = require("components/core/TextInput");
var TextTemplate = require("components/core/TextTemplate");
var User = require("utils/User");

require("css/LoginForm.less");
var LoginViewText = require("text/LoginViewText.md");

<<<<<<< HEAD
var LoginView = React.createClass({
  mixins: [ReactRouter.History],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
    shake: React.PropTypes.func,
  },

  getInitialState: function () {
=======
class LoginView extends React.Component {
  getInitialState() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return {
      error: null,
      username: "",
      password: "",
      loading: false,
    };
  }

<<<<<<< HEAD
  componentWillMount: function () {
=======
  componentWillMount() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    var { user } = this.props;
    if (User.isAnonymous(user)) {
      return;
    }
    if (User.isAdvisor(user)) {
<<<<<<< HEAD
      this.history.pushState(null, "/advisor/profile");
=======
      this.context.history.pushState(null, "/advisor/profile");
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    }
  }

<<<<<<< HEAD
  render: function () {
=======
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <OuterView header={this.renderHeader()}>
        <form id="login" className="login-form" onSubmit={this._handleSubmit}>
          <div className="login-fields">
            <TextInput
              name="username"
              placeholder="Username"
              value={this.state.username}
              onChange={this._handleUsernameChange}
            />
            <TextInput
              type="password"
              name="password"
              placeholder="Password"
              value={this.state.password}
              onChange={this._handlePasswordChange}
            />
          </div>
          <div className="login-register">
            <Button color="blue" loading={this.state.loading} type="submit">
              Log In
            </Button>
            <Button color="green" href="/register">
              Register for BMUN
            </Button>
          </div>
          <NavLink direction="left" href="/password">
            Forgot your password?
          </NavLink>
          {this.renderError()}
        </form>
      </OuterView>
    );
  }

<<<<<<< HEAD
  renderHeader: function () {
=======
  renderHeader() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    var conference = this.context.conference;
    return (
      <div className="logo">
        <hr />
        <TextTemplate
          conferenceStartMonth={conference.start_date["month"]}
          conferenceStartDay={conference.start_date["day"]}
          conferenceEndDay={conference.end_date["day"]}
          conferenceStartYear={conference.start_date["year"]}
        >
          {LoginViewText}
        </TextTemplate>
      </div>
    );
  }

<<<<<<< HEAD
  renderError: function () {
=======
  renderError() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    if (this.state.error) {
      return <StatusLabel status="error">{this.state.error}</StatusLabel>;
    }

    return null;
  }

<<<<<<< HEAD
  _handlePasswordChange: function (password) {
    this.setState({ password });
  },

  _handleUsernameChange: function (username) {
    this.setState({ username });
  },

  _handleSubmit: function (event) {
=======
  _handlePasswordChange(password) {
    this.setState({ password });
  }

  _handleUsernameChange(username) {
    this.setState({ username });
  }

  _handleSubmit(event) {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    this.setState({ loading: true });
    ServerAPI.login(this.state.username, this.state.password).then(
      this._handleSuccess,
      this._handleError
    );
    event.preventDefault();
  }

<<<<<<< HEAD
  _handleSuccess: function (responseJSON) {
=======
  _handleSuccess(responseJSON) {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    CurrentUserActions.login(responseJSON);
  }

<<<<<<< HEAD
  _handleError: function (responseJSON) {
=======
  _handleError(responseJSON) {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    if (!responseJSON.detail) {
      return;
    }

    this.setState(
      {
        error: responseJSON.detail,
        loading: false,
      },
      () => {
        this.context.shake && this.context.shake();
      }
    );
  }
}

LoginView.contextTypes = {
  conference: React.PropTypes.shape(ConferenceContext),
  shake: React.PropTypes.func,
  history: PropTypes.history,
};

module.exports = LoginView;
