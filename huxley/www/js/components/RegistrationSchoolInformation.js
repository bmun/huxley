/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var RegistrationTextInput = require('components/RegistrationTextInput');
var _accessSafe = require('utils/_accessSafe');

const RegistrationSchoolInformation = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    errors: React.PropTypes.object,
    schoolInformation: React.PropTypes.object,
    handleInternationalChange: React.PropTypes.func,
    schoolInternational: React.PropTypes.bool,
  },

  shouldComponentUpdate: function(nextProps, nextState) {
    for (let key in this.props.schoolInformation) {
      if (this.props.schoolInformation[key] !== nextProps.schoolInformation[key]) {
        return true;
      }
    }
    return this.props.schoolInternational !== nextProps.schoolInternational;
  },

  render: function() {
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessSchool = _accessSafe.bind(this, this.props.schoolInformation);
    return (
      <div id="school_information">
        <h3>School Information</h3>
        <p className="instructions">Where is your school located?</p>
        <ul>
          <li>
            <label>
              <input
                type="radio"
                value=''
                onChange={this.props.handleInternationalChange}
                checked={!this.props.schoolInternational}
              /> United States of America
            </label>
          </li>
          <li>
            <label>
              <input
                type="radio"
                value='international'
                onChange={this.props.handleInternationalChange}
                checked={this.props.schoolInternational}
              /> International
            </label>
          </li>
        </ul>
        <RegistrationTextInput
          errors={accessErrors('school_name')}
          placeholder="Official School Name"
          onChange={accessHandlers('school_name')}
          value={accessSchool('school_name')}
        />
        <RegistrationTextInput
          errors={accessErrors('school_address')}
          placeholder="Street Address"
          onChange={accessHandlers('school_address')}
          value={accessSchool('school_address')}
        />
        <RegistrationTextInput
          errors={accessErrors('school_city')}
          placeholder="City"
          onChange={accessHandlers('school_city')}
          value={accessSchool('school_city')}
        />
        <RegistrationTextInput
          errors={accessErrors('school_state')}
          placeholder="State"
          onChange={accessHandlers('school_state')}
          value={accessSchool('school_state')}
        />
        <RegistrationTextInput
          errors={accessErrors('school_zip')}
          placeholder="Zip"
          onChange={accessHandlers('school_zip')}
          value={accessSchool('school_zip')}
        />
        <RegistrationTextInput
          errors={accessErrors('school_country')}
          placeholder="Country"
          onChange={accessHandlers('school_country')}
          value={accessSchool('school_country')}
          disabled={!this.props.schoolInternational}
          isControlled={true}
        />
      </div>
    );
  },
});

module.exports = RegistrationSchoolInformation;
