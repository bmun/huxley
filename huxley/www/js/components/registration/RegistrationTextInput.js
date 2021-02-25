/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var { TextInput } = require("components/core/TextInput");
var { StatusLabel } = require("components/core/StatusLabel");

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
  errors: PropTypes.arrayOf(PropTypes.string),
  onChange: PropTypes.func,
  placeholder: PropTypes.string,
  value: PropTypes.string,
  type: PropTypes.oneOf(["text", "password"]),
};

export { RegistrationTextInput };
