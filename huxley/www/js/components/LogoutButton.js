/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var React = require("react");
=======
import React from "react";
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e

var Button = require("components/core/Button");
var CurrentUserActions = require("actions/CurrentUserActions");
var ServerAPI = require("lib/ServerAPI");

<<<<<<< HEAD
var LogoutButton = React.createClass({
  getInitialState: function () {
=======
class LogoutButton extends React.Component {
  getInitialState() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return {
      loggingOut: false,
    };
  }

<<<<<<< HEAD
  render: function () {
=======
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <Button
        color="blue"
        size="small"
        loading={this.state.loggingOut}
        onClick={this._handleLogout}
      >
        Log Out
      </Button>
    );
  }

<<<<<<< HEAD
  _handleLogout: function (e) {
=======
  _handleLogout(e) {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    this.setState({ loggingOut: true });
    ServerAPI.logout().then(this._handleLogoutSuccess);
  }

<<<<<<< HEAD
  _handleLogoutSuccess: function (responseJSON) {
=======
  _handleLogoutSuccess(responseJSON) {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    CurrentUserActions.logout();
  }
}

module.exports = LogoutButton;
