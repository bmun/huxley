/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var { TextInput } = require("components/core/TextInput");
var { formatPhone } = require("utils/formatPhone");

class PhoneInput extends React.Component {
  componentDidUpdate(prevProps, prevState) {
    if (prevProps.isInternational !== this.props.isInternational) {
      var number = this._formatValue(
        this.props.value,
        this.props.isInternational
      );
      this.props.onChange && this.props.onChange(number);
    }
  }

  render() {
    return (
      <TextInput
        {...this.props}
        isControlled={true}
        placeholder="Phone Number"
        onChange={this._handleChange}
      />
    );
  }

  _handleChange = (value) => {
    var number = this._formatValue(value, this.props.isInternational);
    this.props.onChange && this.props.onChange(number);
  };

  _formatValue = (value, isInternational) => {
    var value = value || "";
    return isInternational
      ? value.replace(/[^0-9+\(\)\-\s]/, "")
      : formatPhone(value);
  }
}

PhoneInput.propTypes = {
  onChange: PropTypes.func,
  value: PropTypes.string,
  isInternational: PropTypes.bool.isRequired,
};

export { PhoneInput };
