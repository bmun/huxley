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
      visible: false,
    };
  },

  render: function() {
    var user = this.props.user.getData();
    return (
      <div>
        <div id="headerwrapper" className="transparent rounded-bottom">
          <div id="header">
            <ul id="right">
              <li>
                Logged in as
                &nbsp;
                <strong>{user.first_name} {user.last_name}</strong>
              </li>
              <li>
                <a id="changepassword-link" onClick={this._handleClick}>
                  Change Password
                </a>
              </li>
              <li id="logout" className="topbarbutton">
                <LogoutButton />
              </li>
            </ul>
            <div id="left">
              <strong>HUXLEY</strong>
              &middot;
              A Conference Management Tool by BMUN
              &middot; <strong>for {this.props.user.isAdvisor() ? "Advisors" :
                "Chairs"} </strong>
            </div>
          </div>
        </div>
        <ChangePasswordView isVisible={this.state.visible} />
      </div>
    );
  },

  _handleClick: function() {
    this.setState({visible: !this.state.visible});
  },
});

module.exports = TopBar;
