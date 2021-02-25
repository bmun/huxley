/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var {
  RegistrationPhoneInput,
} = require("components/registration/RegistrationPhoneInput");
var {
  RegistrationTextInput,
} = require("components/registration/RegistrationTextInput");
var { _accessSafe } = require("utils/_accessSafe");

class RegistrationSecondaryContact extends React.Component {
  render() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessSecondary = _accessSafe.bind(
      this,
      this.props.secondaryContactInformation
    );
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    return (
      <div id="secondary_contact">
        <h3>Secondary Contact</h3>
        <p className="instructions">Please make sure to fill out all fields.</p>
        {this.props.renderContactGenderField("secondary_gender")}
        <RegistrationTextInput
          errors={accessErrors("secondary_name")}
          placeholder="Name"
          onChange={accessHandlers("secondary_name")}
          value={accessSecondary("secondary_name")}
        />
        <RegistrationTextInput
          errors={accessErrors("secondary_email")}
          placeholder="Email"
          onChange={accessHandlers("secondary_email")}
          value={accessSecondary("secondary_email")}
        />
        <RegistrationPhoneInput
          errors={accessErrors("secondary_phone")}
          onChange={accessHandlers("secondary_phone")}
          value={accessSecondary("secondary_phone")}
          isInternational={this.props.isInternational}
        />
        {this.props.renderContactTypeField("secondary_type")}
      </div>
    );
  }
}

RegistrationSecondaryContact.propTypes = {
  handlers: PropTypes.object,
  secondaryContactInformation: PropTypes.object,
  errors: PropTypes.object,
  renderContactGenderField: PropTypes.func,
  renderContactTypeField: PropTypes.func,
  isInternational: PropTypes.bool,
};

export { RegistrationSecondaryContact };
