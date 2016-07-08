/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var cx = require('classnames');
var React = require('react');

var ChangePasswordView = require('./ChangePasswordView');
var LogoutButton = require('./LogoutButton');

var TopBar = React.createClass({
  getInitialState: function() {
    return {
      changePasswordVisible: false,
    };
  },

  componentDidMount: function() {
    document.addEventListener('click', this._hideDropdown);
  },

  componentWillUnmount: function() {
    document.removeEventListener('click', this._hideDropdown);
  },

  render: function() {
    var {user} = this.props;

    return (
      <div>
        <div className="top-bar-wrapper transparent">
          <div className="top-bar">
            <ul className="right">
              <li className="white">
                {user.first_name} {user.last_name}
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
            </div>
          </div>
        </div>
        <ChangePasswordView
          isVisible={this.state.changePasswordVisible}
          onClick={this._handleDropdownClick}
          onSuccess={this._hideDropdown}
        />
      </div>
    );
  },

  _handleChangePasswordClick: function(e) {
    e.preventDefault();
    this._stopPropagation(e);
    this.setState({
      changePasswordVisible: !this.state.changePasswordVisible
    });
  },

  _handleDropdownClick: function(e) {
    this._stopPropagation(e);
  },

  _hideDropdown: function() {
    this.setState({changePasswordVisible: false});
  },

  _stopPropagation: function(e) {
    e.stopPropagation();

    // TODO: display a warning if stopImmediatePropagation isn't supported.
    var ne = e.nativeEvent;
    ne.stopImmediatePropagation && ne.stopImmediatePropagation();
  },
});

module.exports = TopBar;
