/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/Button');
var NavLink = require('components/NavLink');
var OuterView = require('components/OuterView');
var ServerAPI = require('lib/ServerAPI');
var StatusLabel = require('components/StatusLabel');
var TextInput = require('components/TextInput');

require('css/LoginForm.less');

var ForgotPasswordView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  contextTypes: {
    shake: React.PropTypes.func,
  },

  getInitialState: function() {
    return {
      username: '',
      error: false,
      loading: false
    };
  },

  render: function() {
    return (
      <OuterView>
        <h1>Forgot your Password?</h1>
        <p>No problem. Just enter your username below, and we'll send a
        temporary password to your email address.</p>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
        <hr />
        <form
          className="login-form password-reset"
          onSubmit={this._handleSubmit}>
          <div className="login-fields">
            <TextInput
              placeholder="Username or Email"
              value={this.state.username}
              onChange={this._handleUsernameChange}
            />
          </div>
          <Button
            color="green"
            loading={this.state.loading}>
            Reset Password
          </Button>
          <span className="help-text">We'll email you a new one.</span>
          {this.renderError()}
        </form>
      </OuterView>
    );
  },

  renderError: function() {
    if (this.state.error) {
      return (
        <StatusLabel status="error">
          Sorry, we couldn't find a user for the username given.
        </StatusLabel>
      );
    }
  },

  _handleUsernameChange: function(username) {
    this.setState({username});
  },

  _handleSubmit: function(event) {
    this.setState({loading: true});
    ServerAPI.resetPassword(this.state.username).then(
      this._handleSuccess,
      this._handleError,
    );
    event.preventDefault();
  },

  _handleSuccess: function(response) {
    this.history.pushState(null, '/password/reset');
  },

  _handleError: function(response) {
    if (!response.detail) {
      return;
    }

    this.setState({
      error: "Sorry, we couldn't find a user with that username.",
      loading: false
    }, () => {
      this.context.shake && this.context.shake();
    });
  },
});

module.exports = ForgotPasswordView;
