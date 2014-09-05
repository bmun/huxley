/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var ChangePasswordView = require('./ChangePasswordView');
var LogoutButton = require('./LogoutButton');

var TopBar = React.createClass({
  getInitialState: function() {
    return {
      changePasswordVisible: false,
    };
  },

  render: function() {
    var user = this.props.user.getData();
    var cx = React.addons.classSet;

    return (
      <div>
        <div className="top-bar-wrapper transparent">
          <div className="top-bar">
            <ul className="right">
              <li>
                Logged in as
                &nbsp;
                <span className="white">
                  {user.first_name} {user.last_name}
                </span>
              </li>
              <li>
                <a
                  className={cx({
                    'change-password-link': true,
                    'active': this.state.changePasswordVisible,
                  })}
                  href="#"
                  onClick={this._handleChangePasswordClick}>
                  Change Password
                </a>
              </li>
              <li>
                <LogoutButton />
              </li>
            </ul>
            <div className="left">
              <span className="title white">Huxley</span>
              &nbsp;
              &middot;
              &nbsp;
              <span>A Conference Management Tool by BMUN</span>
              &nbsp;
              &middot;
              &nbsp;
              <em className="white">for {this._getUserType()}</em>
            </div>
          </div>
        </div>
        <ChangePasswordView
          isVisible={this.state.changePasswordVisible}
          onSuccess={this._handleChangePasswordSuccess}
        />
      </div>
    );
  },

  _handleChangePasswordSuccess: function() {
    this.setState({changePasswordVisible: false});
  },

  _getUserType: function() {
    return this.props.user.isAdvisor() ? 'Advisors' : 'Chairs';
  },

  _handleChangePasswordClick: function() {
    this.setState({
      changePasswordVisible: !this.state.changePasswordVisible
    });
  },
});

module.exports = TopBar;
