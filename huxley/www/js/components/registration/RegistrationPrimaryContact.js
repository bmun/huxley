/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var {RegistrationPhoneInput} = require("components/registration/RegistrationPhoneInput");
var {RegistrationTextInput} = require("components/registration/RegistrationTextInput");
var {_accessSafe} = require("utils/_accessSafe");

class RegistrationPrimaryContact extends React.Component {
  render() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessPrimary = _accessSafe.bind(
      this,
      this.props.primaryContactInformation
    );
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    return (
      <div id="primary_contact">
        <h3>Primary Contact</h3>
        <p className="instructions">Please make sure to fill out all fields.</p>
        {this.props.renderContactGenderField("primary_gender")}
        <RegistrationTextInput
          errors={accessErrors("primary_name")}
          placeholder="Name"
          onChange={accessHandlers("primary_name")}
          value={accessPrimary("primary_name")}
        />
        <RegistrationTextInput
          errors={accessErrors("primary_email")}
          placeholder="Email"
          onChange={accessHandlers("primary_email")}
          value={accessPrimary("primary_email")}
        />
        <RegistrationPhoneInput
          errors={accessErrors("primary_phone")}
          onChange={accessHandlers("primary_phone")}
          value={accessPrimary("primary_phone")}
          isInternational={this.props.isInternational}
        />
        {this.props.renderContactTypeField("primary_type")}
      </div>
    );
  }
}

RegistrationPrimaryContact.propTypes = {
  handlers: PropTypes.object,
  primaryContactInformation: PropTypes.object,
  errors: PropTypes.object,
  renderContactGenderField: PropTypes.func,
  renderContactTypeField: PropTypes.func,
  isInternational: PropTypes.bool,
};

export {RegistrationPrimaryContact};
