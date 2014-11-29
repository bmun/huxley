/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var React = require('react/addons');

var Button = require('./Button');

var ChangePasswordView = React.createClass({
  mixins: [React.addons.LinkedStateMixin],

  propTypes: {
    isVisible: React.PropTypes.bool.isRequired,
    onClick: React.PropTypes.func,
    onSuccess: React.PropTypes.func.isRequired,
  },

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

  componentWillReceiveProps: function(nextProps) {
    this.setState(this.getInitialState());
  },

  render: function() {
    var cx = React.addons.classSet;
    return (
      <div
        className={cx({
          'change-password': true,
          'rounded-bottom': true,
           'transparent': true,
           'visible': this.props.isVisible,
        })}
        onClick={this._handleDropdownClick}>
        <form onSubmit={this._handleSubmit}>
          <input
            type="password"
            className="rounded-small"
            valueLink={this.linkState('currentPassword')}
          />
          <label>Current Password</label>
          <input
            type="password"
            className="rounded-small"
            valueLink={this.linkState('newPassword')}
          />
          <label>New Password</label>
          <input
            type="password"
            className="rounded-small"
            valueLink={this.linkState('newPassword2')}
          />
          <label>New Password (again)</label>
          <Button
            type="submit"
            color="green"
            size="small"
            loading={this.state.loading}>
            Change Password
          </Button>
        </form>
        {this.renderMessage()}
      </div>
    );
  },

  renderMessage: function() {
    if (!this.state.message) {
      return null;
    }

    return (
      <div className="message">
        <label className={this.state.success ? 'success' : 'error'}>
          {this.state.message}
        </label>
      </div>
    );
  },

  onSuccess: function() {
    setTimeout(this.props.onSuccess, 750);
  },

  _handleSubmit: function(event) {
    if (this.state.newPassword != this.state.newPassword2) {
      this.setState({
        message: 'Please enter the same password again',
        success: false,
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
      loading: false,
      success: true,
      message: 'Password changed!',
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
    }, this.onSuccess);
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    this.setState({
      loading: false,
      message: response.detail,
      success: false,
    });
  },

  _handleDropdownClick: function(e) {
    this.props.onClick && this.props.onClick(e);
  },
});

module.exports = ChangePasswordView;
