/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var LogoutButton = require('./LogoutButton');

var TopBar = React.createClass({
  render: function() {
    var user = this.props.user.getData();
    return (
      <div id="headerwrapper" className="transparent rounded-bottom">
        <div id="header">
          <ul id="right">
            <li>
              Logged in as
              <span className="advisorfirstname bold"> {user.first_name}</span>
              &nbsp;<span className="advisorlastname bold"> {user.last_name}
              </span>
            </li>
            <li id="changepassword-link">Change Password</li>
            <li id="logout" className="topbarbutton">
              <LogoutButton />
            </li>
          </ul>
          <div id="left">
            <strong>HUXLEY</strong> &middot; A Conference Management Tool by
            BMUN &middot; <span className="usertype bold">for {user.user_type
              === 1 ? "Advisors" : "Chairs"} </span>
          </div>
        </div>
      </div>
    );
  },
});

module.exports = TopBar;
