/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var cx = require('classnames');
var React = require('react');

var Button = require('components/Button');
var ServerAPI = require('lib/ServerAPI');
var StatusLabel = require('components/StatusLabel');

require('css/ChangePasswordView.less');

var ChangePasswordView = React.createClass({

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
            value={this.state.currentPassword}
            onChange={this._handleCurrentPasswordChange}
          />
          <label>Current Password</label>
          <input
            type="password"
            className="rounded-small"
            value={this.state.newPassword}
            onChange={this._handleNewPasswordChange}
          />
          <label>New Password</label>
          <input
            type="password"
            className="rounded-small"
            value={this.state.newPassword2}
            onChange={this._handleNewPassword2Change}
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
      <StatusLabel status={this.state.success ? 'success' : 'error'}>
        {this.state.message}
      </StatusLabel>
    );
  },

  onSuccess: function() {
    setTimeout(this.props.onSuccess, 750);
  },

  _handleCurrentPasswordChange: function(event) {
    this.setState({currentPassword: event.target.value});
  },

  _handleNewPasswordChange: function(event) {
    this.setState({newPassword: event.target.value});
  },

  _handleNewPassword2Change: function(event) {
    this.setState({newPassword2: event.target.value});
  },

  _handleSubmit: function(event) {
    if (this.state.newPassword != this.state.newPassword2) {
      this.setState({
        message: 'Please enter the same password again',
        success: false,
      });
    } else {
      this.setState({loading: true});
      const {currentPassword, newPassword} = this.state;
      ServerAPI.changePassword(currentPassword, newPassword).then(
        this._handleSuccess,
        this._handleError,
      );
      event.preventDefault();
    }
  },

  _handleSuccess: function(response) {
    this.setState({
      loading: false,
      success: true,
      message: 'Password changed!',
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
    }, this.onSuccess);
  },

  _handleError: function(response) {
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
