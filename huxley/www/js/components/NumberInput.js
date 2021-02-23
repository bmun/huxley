/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

"use strict";

import React from "react";
var { TextInput } = require("components/core/TextInput");

type NumberInputProps = {
  defaultValue?: string,
  onChange: (any) => void,
  value?: string,
  placeholder?: string,
}
class NumberInput extends React.Component<NumberInputProps> {
  render(): React$Element<any> {
    return (
      <TextInput
        {...this.props}
        isControlled={true}
        onChange={this._handleChange}
      />
    );
  }

  _handleChange: (any) => void = (value) => {
    this.props.onChange && this.props.onChange(value.replace(/[^\d]/, ""));
  };
}

export { NumberInput };
