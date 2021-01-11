/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

var TextInput = require("components/core/TextInput");
var StatusLabel = require("components/core/StatusLabel");

class RegistrationTextInput extends React.Component {
  render() {
    const { errors, ...inputProps } = this.props;
    return (
      <div className="reg-field">
        <TextInput {...inputProps} />
        {errors &&
          errors.map((error) => (
            <StatusLabel status="error">{error}</StatusLabel>
          ))}
      </div>
    );
  }
}

RegistrationTextInput.propTypes = {
  errors: React.PropTypes.arrayOf(React.PropTypes.string),
  onChange: React.PropTypes.func,
  placeholder: React.PropTypes.string,
  value: React.PropTypes.string,
  type: React.PropTypes.oneOf(["text", "password"]),
};

module.exports = RegistrationTextInput;
