/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NavLink = require('./NavLink');
var OuterView = require('./OuterView');

var RegistrationWaitlistView = React.createClass({
  render: function() {
    return (
      <OuterView>
        <div class="letter">
          <p>
            Thank you for your interest in participating in the sixty-third
            session of Berkeley Model United Nations! You are currently on our
            wait list and will be updated on your team's status as spots become
            available again. We thank you for your patience in advance and hope
            to see you at Berkeley next February!
          </p>
        </div>
        <hr />
        <NavLink direction="right" href="/login">
          Proceed to Login
        </NavLink>
      </OuterView>
    );
  }
});

module.exports = RegistrationWaitlistView;
