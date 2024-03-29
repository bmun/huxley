/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var {
  RegistrationTextInput,
} = require("components/registration/RegistrationTextInput");
var { _accessSafe } = require("utils/_accessSafe");

class RegistrationSchoolInformation extends React.Component {
  shouldComponentUpdate(nextProps, nextState) {
    for (let key in this.props.schoolInformation) {
      if (
        this.props.schoolInformation[key] !== nextProps.schoolInformation[key]
      ) {
        return true;
      }
    }

    for (let key in this.props.errors) {
      if (this.props.errors[key] !== nextProps.errors[key]) {
        return true;
      }
    }

    return this.props.schoolInternational !== nextProps.schoolInternational;
  }

  render() {
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
                value=""
                onChange={this.props.handleInternationalChange}
                checked={!this.props.schoolInternational}
              />{" "}
              United States of America
            </label>
          </li>
          <li>
            <label>
              <input
                type="radio"
                value="international"
                onChange={this.props.handleInternationalChange}
                checked={this.props.schoolInternational}
              />{" "}
              International
            </label>
          </li>
        </ul>
        <RegistrationTextInput
          errors={accessErrors("school_name")}
          placeholder="Official School Name"
          onChange={accessHandlers("school_name")}
          value={accessSchool("school_name")}
        />
        <RegistrationTextInput
          errors={accessErrors("school_address")}
          placeholder="Street Address"
          onChange={accessHandlers("school_address")}
          value={accessSchool("school_address")}
        />
        <RegistrationTextInput
          errors={accessErrors("school_city")}
          placeholder="City"
          onChange={accessHandlers("school_city")}
          value={accessSchool("school_city")}
        />
        <RegistrationTextInput
          errors={accessErrors("school_state")}
          placeholder={this.props.schoolInternational ? "Province" : "State"}
          onChange={accessHandlers("school_state")}
          value={accessSchool("school_state")}
        />
        <RegistrationTextInput
          errors={accessErrors("school_zip")}
          placeholder={this.props.schoolInternational ? "Postal Code" : "Zip"}
          onChange={accessHandlers("school_zip")}
          value={accessSchool("school_zip")}
        />
        <RegistrationTextInput
          errors={accessErrors("school_country")}
          placeholder="Country"
          onChange={accessHandlers("school_country")}
          value={accessSchool("school_country")}
          disabled={!this.props.schoolInternational}
          isControlled={true}
        />
      </div>
    );
  }
}

RegistrationSchoolInformation.propTypes = {
  handlers: PropTypes.object,
  errors: PropTypes.object,
  schoolInformation: PropTypes.object,
  handleInternationalChange: PropTypes.func,
  schoolInternational: PropTypes.bool,
};

export { RegistrationSchoolInformation };
