/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var Button = require('./Button');
var NavLink = require('./NavLink');
var OuterView = require('./OuterView');

var ForgotPasswordView = React.createClass({
  mixins: [React.addons.LinkedStateMixin],

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
        <NavLink direction="left" href="/www/login">
          Back to Login
        </NavLink>
        <hr />
        <form
          className="login-form"
          id="password-reset"
          onSubmit={this._handleSubmit}>
          <div className="login-fields">
            <input
              className="text empty"
              type="text"
              placeholder="Username or Email"
              valueLink={this.linkState('username')}
            />
          </div>
          <Button
            className="reset-password-button"
            color="green"
            loading={this.state.loading}>
            Reset Password
          </Button>
          <span className="help-text">We'll email you a new one.</span>
          <div id="errorcontainer">
            {this.renderError()}
          </div>
        </form>
      </OuterView>
    );
  },

  renderError: function() {
    if (this.state.error) {
      return (
        <label className="error">
          Sorry, we couldn't find a user for the username given.
        </label>
      );
    }
  },

  _handleSubmit: function(event) {
    // TODO: build the reset password API and hook it up here.
    this.setState({loading: true});
    event.preventDefault();
  }
});

module.exports = ForgotPasswordView;
