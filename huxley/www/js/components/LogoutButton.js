/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

var {Button} = require("components/core/Button");
var {CurrentUserActions} = require("actions/CurrentUserActions");
var {ServerAPI} = require("lib/ServerAPI");

class LogoutButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggingOut: false,
    };
  }

  render() {
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

  _handleLogout(e) {
    this.setState({ loggingOut: true });
    ServerAPI.logout().then(this._handleLogoutSuccess);
  }

  _handleLogoutSuccess(responseJSON) {
    CurrentUserActions.logout();
  }
}

export {LogoutButton};
