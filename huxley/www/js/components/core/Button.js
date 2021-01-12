/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import cx from "classnames";
import React from "react";
import {Link} from "react-router-dom";
import PropTypes from "prop-types";

require("css/Button.less");

class Button extends React.Component {
  render() {
    var ButtonComponent = this.props.href ? Link : "button";

    return (
      <ButtonComponent
        {...this.props}
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

Button.propTypes = {
  color: PropTypes.oneOf(["blue", "green", "yellow", "red"]),
  href: PropTypes.string,
  loading: PropTypes.bool,
  size: PropTypes.oneOf(["small", "medium", "large"]),
  success: PropTypes.bool,
};


