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
var InnerView = require('./InnerView');

var AdvisorProfileView = React.createClass({
  getInitialState: function() {
    return {
      loggingOut: false // TODO: logout button should be its own component.
    };
  },

  render: function() {
    var cx = React.addons.classSet;
    return (
      <InnerView>
        <p>This is the advisor profile view. It does not do anything yet.</p>
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
      </InnerView>
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

module.exports = AdvisorProfileView;
