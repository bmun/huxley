/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var RegistrationTextInput = require('components/RegistrationTextInput');
var _accessSafe = require('utils/_accessSafe');

const RegistrationSecondaryContact = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    secondaryContactInformation: React.PropTypes.object,
    errors: React.PropTypes.object,
    renderContactGenderField: React.PropTypes.func,
    renderContactTypeField: React.PropTypes.func,
    isInternational: React.PropTypes.bool,
  },

  shouldComponentUpdate: function(nextProps, nextState) {
    for (let key in this.props.secondaryContactInformation) {
      if(this.props.secondaryContactInformation[key] !== nextProps.secondaryContactInformation[key]) {
        return true;
      }
    }
    return this.props.isInternational !== nextProps.isInternational;
  },

  render: function() { 
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessSecondary = _accessSafe.bind(this, this.props.secondaryContactInformation);
    var accessErrors = _accessSafe.bind(this, this.props.errors)
    return (
      <div id='secondary_contact'>
        <h3>Secondary Contact</h3>
        {this.props.renderContactGenderField('secondary_gender')}
        <RegistrationTextInput
          errors={accessErrors('secondary_name')}
          placeholder="Name" 
          onChange={accessHandlers('secondary_name')}
          value={accessSecondary('secondary_name')}
        />
        <RegistrationTextInput 
          errors={accessErrors('secondary_email')}
          placeholder="Email" 
          onChange={accessHandlers('secondary_email')}
          value={accessSecondary('secondary_email')}
        />
        <RegistrationTextInput 
          errors={accessErrors('secondary_phone')}
          onChange={accessHandlers('secondary_phone')}
          value={accessSecondary('secondary_phone')}
          placeholder="Phone Number" 
          isInternational={this.props.isInternational}
        />
        {this.props.renderContactTypeField('secondary_type')}
      </div>
    );
  },
});

module.exports = RegistrationSecondaryContact;

