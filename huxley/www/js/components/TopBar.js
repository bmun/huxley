/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import React from 'react';
import cx from 'classnames';

var ChangePasswordView = require('components/ChangePasswordView');
var LogoutButton = require('components/LogoutButton');

require('css/TopBar.less');

class TopBar extends React.Components {
  getInitialState() {
    return {
      changePasswordVisible: false,
    };
  }

  componentDidMount() {
    document.addEventListener('click', this._hideDropdown);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this._hideDropdown);
  }

  render() {
    var {user} = this.props;

    return (
      <div>
        <div className="top-bar-wrapper">
          <div className="top-bar">
            <ul className="right">
              <li className="white">
                {`${user.first_name} ${user.last_name}`}
              </li>
              <li>
                <a
                  className={cx({
                    'change-password-link': true,
                    active: this.state.changePasswordVisible,
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
              &nbsp; &middot; &nbsp;
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
  }

  _handleChangePasswordClick(e) {
    e.preventDefault();
    this._stopPropagation(e);
    this.setState({
      changePasswordVisible: !this.state.changePasswordVisible,
    });
  }

  _handleDropdownClick(e) {
    this._stopPropagation(e);
  }

  _hideDropdown() {
    this.setState({changePasswordVisible: false});
  }

  _stopPropagation(e) {
    e.stopPropagation();

    // TODO: display a warning if stopImmediatePropagation isn't supported.
    var ne = e.nativeEvent;
    ne.stopImmediatePropagation && ne.stopImmediatePropagation();
  }
};

module.exports = TopBar;
