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
        className="change-passwordrounded-bottom transparent">
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
      </div>
    );
  },

  _handleSubmit: function(event) {
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
  },

  _handleSuccess: function(data, status, jqXHR) {
    console.log('success!');
  },

  _handleError: function(jqXHR, status, error) {
    console.log('error');
  },
});

module.exports = ChangePasswordView;
