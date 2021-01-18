/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import cx from "classnames";
import PropTypes from "prop-types";

require("css/TextInput.less");

/**
 * TextInput is uncontrolled by default to preserve cursor position.
 * Controlled inputs cannot preserve cursor position upon rendering.
 * See issue #519.
 */
class TextInput extends React.Component {
  render() {
    return (
      <input
        {...this.props}
        className={cx("text-input", this.props.className)}
        onChange={this._handleChange}
        type={this.props.type || "text"}
        value={this.props.isControlled ? this.props.value : undefined}
      />
    );
  }
  _handleChange = (event) => {
    this.props.onChange && this.props.onChange(event.target.value);
  };
}

TextInput.propTypes = {
  defaultValue: PropTypes.string,
  isControlled: PropTypes.bool,
  onChange: PropTypes.func,
  placeholder: PropTypes.string,
  value: PropTypes.string,
  type: PropTypes.oneOf(["text", "password"]),
};

export { TextInput };
