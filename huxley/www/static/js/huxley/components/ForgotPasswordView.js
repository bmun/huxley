/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var React = require('react/addons');
var Router = require('react-router');

var Button = require('./Button');
var NavLink = require('./NavLink');
var OuterView = require('./OuterView');

require('jquery-ui/effect-shake');

var ForgotPasswordView = React.createClass({
  mixins: [
    React.addons.LinkedStateMixin,
    Router.Navigation,
  ],

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
    this.setState({loading: true});
    $.ajax({
      type: 'POST',
      url: '/api/users/me/password',
      data: {
        username: this.state.username
      },
      success: this._handleSuccess,
      error: this._handleError
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    this.transitionTo('/password/reset');
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    if (!response.detail) {
      return;
    }

    this.setState({
      error: "Sorry, we couldn't find a user with that username.",
      loading: false
    }, function() {
      $(this.getDOMNode()).effect(
        'shake',
        {direction: 'up', times: 2, distance: 2},
        250
      );
    }.bind(this));
  },
});

module.exports = ForgotPasswordView;
