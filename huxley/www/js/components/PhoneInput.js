/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
//@flow
"use strict";

import React from "react";

var { TextInput } = require("components/core/TextInput");
var { formatPhone } = require("utils/formatPhone");

type PhoneInputProps = {
  onChange?: (any) => void,
  value?: string,
  isInternational: boolean,
};
class PhoneInput extends React.Component<PhoneInputProps> {
  componentDidUpdate(prevProps: PhoneInputProps, prevState: void) {
    if (prevProps.isInternational !== this.props.isInternational) {
      var number = this._formatValue(
        this.props.value,
        this.props.isInternational
      );
      this.props.onChange && this.props.onChange(number);
    }
  }

  render(): React$Element<any> {
    const {isInternational, ...newProps} = this.props;
    return (
      <TextInput
        {...newProps}
        isControlled={true}
        placeholder="Phone Number"
        onChange={this._handleChange}
      />
    );
  }

  _handleChange: (string) => void = (value) => {
    var number = this._formatValue(value, this.props.isInternational);
    this.props.onChange && this.props.onChange(number);
  };

  _formatValue: (?string, boolean) => string = (value, isInternational) => {
    var valueOrEmpty: string = value ?? "";
    return isInternational
      ? valueOrEmpty.replace(/[^0-9+\(\)\-\s]/, "")
      : formatPhone(value);
  }
}

export { PhoneInput };
