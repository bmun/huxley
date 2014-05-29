/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var $ = require('jquery');
var React = require('react/addons');

var CurrentUserActions = require('../actions/CurrentUserActions');

var LogoutButton = React.createClass({
  getInitialState: function() {
    return {loggingOut: false};
  },

  render: function() {
    var cx = React.addons.classSet;
    return (
      <a
        className={cx({
          'button': true,
          'button-blue': true,
          'login-button': true,
          'rounded-small': true,
          'loading': this.state.loggingOut
        })}
        onClick={this._handleLogout}>
        Log Out
      </a>
    );
  },

  _handleLogout: function(e) {
    this.setState({loggingOut: true});
    $.ajax({
      type: 'DELETE',
      url: '/api/users/me',
      success: this._handleLogoutSuccess,
      error: this._handleLogoutError,
      dataType: 'json'
    });
  },

  _handleLogoutSuccess: function(data, status, jqXHR) {
    console.log('logging out');
    CurrentUserActions.logout();
  },

  _handleLogoutError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    console.log(response.detail);
  }
});

module.exports = LogoutButton;
