/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
//@flow

"use strict";

import React from "react";
import cx from "classnames";

//$FlowFixMe
require("css/TextInput.less");

/**
 * TextInput is uncontrolled by default to preserve cursor position.
 * Controlled inputs cannot preserve cursor position upon rendering.
 * See issue #519.
 */
type TextInputProps = {
  className?: string,
  defaultValue?: string,
  isControlled?: boolean,
  onChange?: (any) => void,
  placeholder?: string,
  value?: string,
  type?: "text" | "password",
};
class TextInput extends React.Component<TextInputProps> {
  render(): React$Element<any> {
    const { isControlled, ...newProps } = this.props;
    return (
      <input
        {...newProps}
        className={cx("text-input", this.props.className)}
        onChange={this._handleChange}
        type={this.props.type || "text"}
        value={this.props.isControlled ? this.props.value : undefined}
      />
    );
  }
  _handleChange: (any) => void = (event) => {
    this.props.onChange && this.props.onChange(event.target.value);
  };
}

export { TextInput };
