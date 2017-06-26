/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NavLink = require('components/NavLink');
var RegistrationViewText = require('text/RegistrationViewText.md');
var TextTemplate = require('components/TextTemplate');

const RegistrationHeader = React.createClass({
  propTypes: {
    session: React.PropTypes.number,
  },

  render: function() {
    return (
      <div>
        <TextTemplate conferenceSession={this.props.session}>
          {RegistrationViewText}
        </TextTemplate>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
      </div>
    );
  },
});

module.exports = RegistrationHeader;
