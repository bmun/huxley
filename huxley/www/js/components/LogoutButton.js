/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var Button = require('components/core/Button');
var CurrentUserActions = require('actions/CurrentUserActions');
var ServerAPI = require('lib/ServerAPI');

var LogoutButton = React.createClass({
  getInitialState: function() {
    return {
      loggingOut: false,
    };
  },

  render: function() {
    return (
      <Button
        color="blue"
        size="small"
        loading={this.state.loggingOut}
        onClick={this._handleLogout}>
        Log Out
      </Button>
    );
  },

  _handleLogout: function(e) {
    this.setState({loggingOut: true});
    ServerAPI.logout().then(this._handleLogoutSuccess);
  },

  _handleLogoutSuccess: function(responseJSON) {
    CurrentUserActions.logout();
  },
});

module.exports = LogoutButton;
