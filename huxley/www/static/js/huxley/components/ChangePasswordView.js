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
      message: '',
      success: false,
      loading: false,
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
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
        {this.renderMessage()}
      </div>
    );
  },

  renderMessage: function() {
    if (this.state.success) {
      return (
        <div id="message">
          <label className="success">Success</label>
        </div>
      );
    } else if (this.state.message) {
      return (
        <div id="message">
          <label className="error">{this.state.message}</label>
        </div>
      );
    }

    return null;
  },

  onSuccess: function() {
    setTimeout(this.props.onSuccess, 2000);
  },

  _handleSubmit: function(event) {
    if (this.state.newPassword != this.state.newPassword2) {
      this.setState({
        message: 'Please enter the same password again',
      });
    } else {
      this.setState({loading: true});
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
      message: '',
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
    }, this.onSuccess);
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    this.setState({message: response.detail});
  },
});

module.exports = ChangePasswordView;
