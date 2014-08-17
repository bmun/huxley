/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var $ = require('jquery');
var React = require('react/addons');

var Button = require('./Button');

var ChangePasswordView = React.createClass({
  mixins: [React.addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      error: null,
      passwordConfirmError: null,
      success: null,
      loading: false,
      currentPassword: null,
      newPassword: null,
      newPassword2: null,
    };
  },

  render: function() {
    if (!this.props.isVisible) {
      return <div />;
    }

    return (
      <div
        id="changepassword-container"
        className="change-password rounded-bottom transparent">
        <form
          id="changepassword"
          onSubmit={this._handleSubmit}>
          <div className="input">
            <label htmlFor="oldpassword">Current Password</label>
            <input
              type="password"
              className="rounded-small"
              valueLink={this.linkState('currentPassword')}
            />
          </div>
          <div className="input">
            <label htmlFor="newpassword">New Password</label>
            <input
              type="password"
              className="rounded-small"
              valueLink={this.linkState('newPassword')}
            />
          </div>
          <div className="input">
            <label htmlFor="newpassword">New Password (again)</label>
            <input
              type="password"
              className="rounded-small"
              valueLink={this.linkState('newPassword2')}
            />
          </div>
          <div className="rounded-small topbarbutton">
            <Button
              type="submit"
              loading={this.state.loading}>
              Change Password!
            </Button>
          </div>
        </form>
        {this.renderSuccess()}
        {this.renderError()}
        {this.renderPasswordConfirmError()}
      </div>
    );
  },

  renderSuccess: function() {
    if (this.state.success) {
      return (
        <div id="message">
          <label className="success">Success</label>
        </div>
      );
    }

    return null;
  },

  renderError: function() {
    if (this.state.error) {
      return (
        <div id="message">
          <label className="error">{this.state.error}</label>
        </div>
      );
    }

    return null;
  },

  renderPasswordConfirmError: function() {
    if (this.state.passwordConfirmError) {
      return (
        <div id="message">
          <label className="error">Please enter the same passoword again.
          </label>
        </div>
      );
    }

    return null;
  },

  _handleSubmit: function(event) {
    if (this.state.newPassword != this.state.newPassword2) {
      this.setState({
        passwordConfirmError: true,
        error: false,
      });
    } else {
      this.setState({
        loading: true,
        passwordConfirmError: false
      });
      $.ajax({
        type: 'PUT',
        url: '/api/users/me/password',
        data: {
          password: this.state.currentPassword,
          new_password: this.state.newPassword,
        },
        success: this._handleSuccess,
        error: this._handleError
      }),
      event.preventDefault();
    }
  },

  _handleSuccess: function(data, status, jqXHR) {
    this.setState({
      success: true,
      error: false,
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
    });
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    this.setState({error: response.detail});
  },
});

module.exports = ChangePasswordView;
