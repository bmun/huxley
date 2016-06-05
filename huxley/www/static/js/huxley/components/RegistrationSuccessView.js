/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var ConferenceContext = require('./ConferenceContext');
var NavLink = require('./NavLink');
var OuterView = require('./OuterView');

var RegistrationSuccessView = React.createClass({

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  render: function() {
    var conference = this.context.conference;
    return (
      <OuterView>
        <div class="letter">
          <h1>Thank You</h1>
          <p>
            Thank you for registering for BMUN {conference.session}! Country assignments will be
            made available soon in your Huxley account. A summary of fees is
            listed below:
          </p>
          <h3>School Registration Fee</h3>
          <ul>
            <li>${conference.registration_fee}</li>
          </ul>
          <h3>Delegate Registration Fee</h3>
          <ul>
            <li>${conference.delegate_fee}</li>
          </ul>
          <h3>Payment Instructions</h3>
          <p>
            <strong>
              We ask that you compile delegate fees into ONE check
            </strong>
            &nbsp;&#8212;
            please do not have your students mail individual checks.
          </p>
          <p>
            Please mail all checks out to:
          </p>
          <div class="address">
            <p><strong>Berkeley Model United Nations</strong>
              <br />
              P.O. Box #4306
              <br />
              Berkeley, CA 94704-0306
            </p>
          </div>
          <p>
            If you have any questions or concerns, please feel free to contact
            me at <a href="mailto:info@bmun.org">info@bmun.org</a>. We look
            forward to seeing you in March!
          </p>
          <p>Sincerely,</p>
          <p class="sender">
            <strong>{conference.external}</strong>
            <br />
            <span class="subtext">
              Under-Secretary General of External Relations
              <br />
              Berkeley Model United Nations, {conference.session}th Session
            </span>
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

module.exports = RegistrationSuccessView;
