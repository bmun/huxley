/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NumberInput = require('components/NumberInput');
var _accessSafe = require('utils/_accessSafe');

const RegistrationSpecialCommitteePreferences = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    errors: React.PropTypes.object,
    specialCommitteePrefValues: React.PropTypes.object,
    renderCommittees: React.PropTypes.func,
  },

  render: function() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessValues = _accessSafe.bind(
      this,
      this.props.specialCommitteePrefValues,
    );
    return (
      <div id="special_committee_preferences">
        <h3>Special Committee Preferences</h3>
        <p className="instructions">
          Would your delegation be interested in being represented in the
          following small/specialized committees? Positions are limited and we
          may not be able to accommodate all preferences. You can find a
          reference to our committees{' '}
          <a href="http://www.bmun.org/committees" target="_blank">
            here
          </a>.
        </p>
        <ul>{this.props.renderCommittees()}</ul>
        <NumberInput
          placeholder="Number of Spanish Speaking Delegates"
          onChange={accessHandlers('num_spanish_speaking_delegates')}
          value={accessValues('num_spanish_speaking_delegates')}
        />
        {accessErrors('num_spanish_speaking_delegates')}
        <NumberInput
          placeholder="Number of Chinese Speaking Delegates"
          onChange={accessHandlers('num_chinese_speaking_delegates')}
          value={accessValues('num_chinese_speaking_delegates')}
        />
        {accessErrors('num_chinese_speaking_delegates')}
      </div>
    );
  },
});

module.exports = RegistrationSpecialCommitteePreferences;
