/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NavLink = require('./NavLink');
var OuterView = require('./OuterView');

var PasswordResetSuccessView = React.createClass({
  render: function() {
    return (
      <OuterView>
        <h1>Your password was reset successfully</h1>
        <p>
          We've sent a temporary password to the email address in your account.
          Please use it to log in and change your password.
        </p>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
      </OuterView>
    );
  }
});

module.exports = PasswordResetSuccessView;
