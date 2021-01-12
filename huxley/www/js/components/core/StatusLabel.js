/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import cx from "classnames";
import PropTypes from "prop-types";

require("css/StatusLabel.less");

class StatusLabel extends React.Component {
  render() {
    return (
      <label
        className={cx({
          "status-label": true,
          "label-success": this.props.status === "success",
          "label-error": this.props.status === "error",
        })}
      >
        {this.props.children}
      </label>
    );
  }
}

StatusLabel.propTypes = {
  status: PropTypes.oneOf(["success", "error"]).isRequired,
};


