/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";
import history from "utils/history";


var {Button} = require("components/core/Button");
var {NavLink} = require("components/NavLink");
var {OuterView} = require("components/OuterView");
var ServerAPI = require("lib/ServerAPI");
var {StatusLabel} = require("components/core/StatusLabel");
var {TextInput} = require("components/core/TextInput");
var {TextTemplate} = require("components/core/TextTemplate");

require("css/LoginForm.less");
var ForgotPasswordViewText = require("text/ForgotPasswordViewText.md");

class ForgotPasswordView extends React.Component {
  getInitialState() {
    return {
      username: "",
      error: false,
      loading: false,
    };
  }

  render() {
    return (
      <OuterView>
        <TextTemplate>{ForgotPasswordViewText}</TextTemplate>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
        <hr />
        <form
          className="login-form password-reset"
          onSubmit={this._handleSubmit}
        >
          <div className="login-fields">
            <TextInput
              placeholder="Username or Email"
              value={this.state.username}
              onChange={this._handleUsernameChange}
            />
          </div>
          <Button color="green" loading={this.state.loading}>
            Reset Password
          </Button>
          <span className="help-text">We'll email you a new one.</span>
          {this.renderError()}
        </form>
      </OuterView>
    );
  }

  renderError() {
    if (this.state.error) {
      return (
        <StatusLabel status="error">
          Sorry, we couldn't find a user for the username given.
        </StatusLabel>
      );
    }
  }

  _handleUsernameChange(username) {
    this.setState({ username });
  }

  _handleSubmit(event) {
    this.setState({ loading: true });
    ServerAPI.resetPassword(this.state.username).then(
      this._handleSuccess,
      this._handleError
    );
    event.preventDefault();
  }

  _handleSuccess(response) {
    history.pushState(null, "/password/reset");
  }

  _handleError(response) {
    if (!response.detail) {
      return;
    }

    this.setState(
      {
        error: "Sorry, we couldn't find a user with that username.",
        loading: false,
      },
      () => {
        this.context.shake && this.context.shake();
      }
    );
  }
}

ForgotPasswordView.contextTypes = {
  shake: PropTypes.func,
};

export {ForgotPasswordView};
