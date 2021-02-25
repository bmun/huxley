/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import { NavLink } from "react-router-dom";
import React from "react";
import PropTypes from "prop-types";

class NavTab extends React.Component {
  render() {
    return (
      <NavLink activeClassName="current" className="tab" to={this.props.href}>
        {this.props.children}
      </NavLink>
    );
  }
}

NavTab.propTypes = {
  href: PropTypes.string.isRequired,
};

export { NavTab };
