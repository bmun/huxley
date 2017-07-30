/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var RegistrationPhoneInput = require('components/registration/RegistrationPhoneInput');
var RegistrationTextInput = require('components/registration/RegistrationTextInput');
var _accessSafe = require('utils/_accessSafe');

const RegistrationPrimaryContact = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    primaryContactInformation: React.PropTypes.object,
    errors: React.PropTypes.object,
    renderContactGenderField: React.PropTypes.func,
    renderContactTypeField: React.PropTypes.func,
    isInternational: React.PropTypes.bool,
  },

  shouldComponentUpdate: function(nextProps, nextState) {
    for (let key in this.props.primaryContactInformation) {
      if (
        this.props.primaryContactInformation[key] !==
        nextProps.primaryContactInformation[key]
      ) {
        return true;
      }
    }
    return this.props.isInternational !== nextProps.isInternational;
  },

  render: function() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessPrimary = _accessSafe.bind(
      this,
      this.props.primaryContactInformation,
    );
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    return (
      <div id="primary_contact">
        <h3>Primary Contact</h3>
        {this.props.renderContactGenderField('primary_gender')}
        <RegistrationTextInput
          errors={accessErrors('primary_name')}
          placeholder="Name"
          onChange={accessHandlers('primary_name')}
          value={accessPrimary('primary_name')}
        />
        <RegistrationTextInput
          errors={accessErrors('primary_email')}
          placeholder="Email"
          onChange={accessHandlers('primary_email')}
          value={accessPrimary('primary_email')}
        />
        <RegistrationPhoneInput
          errors={accessErrors('primary_phone')}
          onChange={accessHandlers('primary_phone')}
          value={accessPrimary('primary_phone')}
          isInternational={this.props.isInternational}
        />
        {this.props.renderContactTypeField('primary_type')}
      </div>
    );
  },
});

module.exports = RegistrationPrimaryContact;
