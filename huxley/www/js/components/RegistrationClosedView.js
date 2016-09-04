/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var ConferenceContext = require('components/ConferenceContext');
var NavLink = require('components/NavLink');
var OuterView = require('components/OuterView');

var RegistrationClosedView = React.createClass({
  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  render: function() {
    var conference = this.context.conference;
    return (
      <OuterView>
        <div className="letter">
          <h1>We're Sorry</h1>
          {conference.registration_waitlist ?
          <p>
            Thank you for your interest in participating in
            BMUN {conference.session}. Registration is now closed
            as we have already reached our maximum capacity. We hope to see you
            at the next BMUN session!
          </p>
          :
          <p>
            Thank you for your interest in BMUN {conference.session}.
            Registration will be open on September 12th at 8 AM.
            If you have any questions please
            contact <a href="mailto:info@bmun.org">info@bmun.org</a>.
            We hope to see you at BMUN 65!
          </p>
          }
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
