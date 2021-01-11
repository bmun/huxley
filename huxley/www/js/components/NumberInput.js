/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
var TextInput = require("components/core/TextInput");

class NumberInput extends React.Component {
  render() {
    return (
      <TextInput
        {...this.props}
        isControlled={true}
        onChange={this._handleChange}
      />
    );
  }

  _handleChange(value) {
    this.props.onChange && this.props.onChange(value.replace(/[^\d]/, ""));
  }
}

NumberInput.propTypes = {
  onChange: React.PropTypes.func,
  value: React.PropTypes.string,
  placeholder: React.PropTypes.string,
};

module.exports = NumberInput;
