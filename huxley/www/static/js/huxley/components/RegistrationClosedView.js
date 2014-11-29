/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NavLink = require('./NavLink');
var OuterView = require('./OuterView');

var RegistrationClosedView = React.createClass({
  render: function() {
    return (
      <OuterView>
        <div className="letter">
          <h1>I'm Sorry</h1>
          <p>
            Thank you for your interest in participating in the sixty-third
            session of Berkeley Model United Nations. Registration is now closed
            as we have already reached our maximum capacity. We hope to see you
            at the next BMUN session!
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

module.exports = RegistrationClosedView;
