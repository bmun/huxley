/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import cx from "classnames";
import React from "react";
import PropTypes from "prop-types";

var Button = require("components/core/Button");
var ServerAPI = require("lib/ServerAPI");
var StatusLabel = require("components/core/StatusLabel");

require("css/ChangePasswordView.less");

class ChangePasswordView extends React.Component {
  getInitialState() {
    return {
      message: "",
      success: false,
      loading: false,
      currentPassword: "",
      newPassword: "",
      newPassword2: "",
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(this.getInitialState());
  }

  render() {
    return (
      <div
        className={cx({
          "change-password": true,
          "rounded-bottom": true,
          transparent: true,
          visible: this.props.isVisible,
        })}
        onClick={this._handleDropdownClick}
      >
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
            loading={this.state.loading}
          >
            Change Password
          </Button>
        </form>
        {this.renderMessage()}
      </div>
    );
  }

  renderMessage() {
    if (!this.state.message) {
      return null;
    }

    return (
      <StatusLabel status={this.state.success ? "success" : "error"}>
        {this.state.message}
      </StatusLabel>
    );
  }
  onSuccess() {
    setTimeout(this.props.onSuccess, 750);
  }

  _handleCurrentPasswordChange(event) {
    this.setState({ currentPassword: event.target.value });
  }

  _handleNewPasswordChange(event) {
    this.setState({ newPassword: event.target.value });
  }

  _handleNewPassword2Change(event) {
    this.setState({ newPassword2: event.target.value });
  }

  _handleSubmit(event) {
    if (this.state.newPassword != this.state.newPassword2) {
      this.setState({
        message: "Please enter the same password again",
        success: false,
      });
    } else {
      this.setState({ loading: true });
      const { currentPassword, newPassword } = this.state;
      ServerAPI.changePassword(currentPassword, newPassword).then(
        this._handleSuccess,
        this._handleError
      );
      event.preventDefault();
    }
  }

  _handleSuccess(response) {
    this.setState(
      {
        loading: false,
        success: true,
        message: "Password changed!",
        currentPassword: "",
        newPassword: "",
        newPassword2: "",
      },
      this.onSuccess
    );
  }

  _handleError(response) {
    this.setState({
      loading: false,
      message: response.detail,
      success: false,
    });
  }

  _handleDropdownClick(e) {
    this.props.onClick && this.props.onClick(e);
  }
}

ChangePasswordView.propTypes = {
  isVisible: PropTypes.bool.isRequired,
  onClick: PropTypes.func,
  onSuccess: PropTypes.func.isRequired,
};


