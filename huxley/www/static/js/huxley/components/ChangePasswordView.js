/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var Button = require('./Button');

var ChangePasswordView = React.createClass({
  render: function() {
    if (this.props.isVisible) {
      return (
        <div id="changepassword-container" className="change-password
        rounded-bottom transparent">
          <form id="changepassword">
            <div className="input">
              <label htmlFor="oldpassword">Current Password</label>
              <input
                type="password"
                className="rounded-small"
                name="oldpassword"
              />
            </div>
            <div className="input">
              <label htmlFor="newpassword">New Password</label>
              <input
                type="password"
                className="rounded-small"
                name="newpassword"
              />
            </div>
            <div className="input">
              <label htmlFor="newpassword">New Password (again)</label>
              <input
                type="password"
                className="rounded-small"
                name="newpassword2"
              />
            </div>
            <div className="rounded-small topbarbutton">
              <Button>Change Password!</Button>
            </div>
          </form>
        </div>
      );
    } else {
      return <div />;
    }
  },
});

module.exports = ChangePasswordView;
