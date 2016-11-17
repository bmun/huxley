/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var ConferenceContext = require('components/ConferenceContext');
var NavLink = require('components/NavLink');
var OuterView = require('components/OuterView');

var RegistrationWaitlistView = React.createClass({

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  render: function() {
    return (
      <OuterView>
        <div class="letter">
          <p>
            Thank you for your interest in participating in
            BMUN {conference.session}! You are currently on our
            wait list and will be updated on your team's status as spots become
            available again. We thank you for your patience in advance and hope
            to see you at Berkeley next March!
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
