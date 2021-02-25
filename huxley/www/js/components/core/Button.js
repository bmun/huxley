/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
//@flow

"use strict";

import cx from "classnames";
import * as React from 'react';
import { Link } from "react-router-dom";

//$FlowFixMe
require("css/Button.less");

type ButtonProps = {
  color?: "blue" | "green" | "yellow" | "red",
  href?: string,
  loading?: boolean,
  size?: "small" | "medium" | "large",
  success?: boolean,
  children?: React.Node,
};
class Button extends React.Component<ButtonProps> {
  render(): React$Element<any> {
    var ButtonComponent = this.props.href ? Link : "button";
    var {loading, success, ...newProps} = this.props;
    return (
      <ButtonComponent
        {...newProps}
        className={cx({
          button: true,
          "button-small": this.props.size == "small",
          "button-large": this.props.size == "large",
          "button-blue": this.props.color == "blue",
          "button-green": this.props.color == "green",
          "button-yellow": this.props.color == "yellow",
          "button-red": this.props.color == "red",
          "rounded-small": true,
          loading: this.props.loading,
          "button-checkmark": this.props.success,
        })}
        disabled={this.props.loading}
        to={this.props.href}
      >
        <span>{this.props.children}</span>
      </ButtonComponent>
    );
  }
}

export { Button };
