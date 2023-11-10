/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import { history } from "utils/history";

const { Button } = require("components/core/Button");
const { CurrentUserActions } = require("actions/CurrentUserActions");
const { CurrentUserStore } = require("stores/CurrentUserStore");
const { NavLink } = require("components/NavLink");
const { OuterView } = require("components/OuterView");
const { ServerAPI } = require("lib/ServerAPI");
const { ShakerContext } = require('components/Shaker');
const { StatusLabel } = require("components/core/StatusLabel");
const { TextInput } = require("components/core/TextInput");
const { TextTemplate } = require("components/core/TextTemplate");
const { User } = require("utils/User");

require("css/LoginForm.less");
var LoginViewText = require("text/LoginViewText.md");

class LoginView extends React.Component {
  static contextType = ShakerContext;

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      username: "",
      password: "",
      loading: false,
    };
  }

  UNSAFE_componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (User.isAnonymous(user)) {
      return;
    }
    if (User.isAdvisor(user)) {
      history.redirect("/advisor/profile");
    }
  }

  render() {
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
            <Button loading={false} color="green" href="/register">
              Register for BMUN's waitlist
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

  renderHeader = () => {
    return (
      <div className="logo">
        <hr />
        <TextTemplate
          conferenceStartMonth={global.conference.start_date["month"]}
          conferenceStartDay={global.conference.start_date["day"]}
          conferenceEndDay={global.conference.end_date["day"]}
          conferenceStartYear={global.conference.start_date["year"]}
        >
          {LoginViewText}
        </TextTemplate>
      </div>
    );
  }

  renderError = () => {
    if (this.state.error) {
      return <StatusLabel status="error">{this.state.error}</StatusLabel>;
    }

    return null;
  };

  _handlePasswordChange = (password) => {
    this.setState({ password });
  };

  _handleUsernameChange = (username) => {
    this.setState({ username });
  };

  _handleSubmit = (event) => {
    this.setState({ loading: true });
    ServerAPI.login(this.state.username, this.state.password).then(
      this._handleSuccess,
      this._handleError
    );
    event.preventDefault();
  };

  _handleSuccess = (responseJSON) => {
    CurrentUserActions.login(responseJSON);
  };

  _handleError = (responseJSON) => {
    if (!responseJSON.detail) {
      return;
    }

    this.setState(
      {
        error: responseJSON.detail,
        loading: false,
      },
      () => {
        this.context && this.context();
      }
    );
  };
}

export { LoginView };
