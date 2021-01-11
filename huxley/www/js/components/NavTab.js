/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

var Link = require("react-router").Link;
<<<<<<< HEAD
var React = require("react");

var NavTab = React.createClass({
  propTypes: {
    href: React.PropTypes.string.isRequired,
  },

  render: function () {
=======
import React from "react";

class NavTab extends React.Component {
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <Link activeClassName="current" className="tab" to={this.props.href}>
        {this.props.children}
      </Link>
    );
  }
}

NavTab.propTypes = {
  href: React.PropTypes.string.isRequired,
};

module.exports = NavTab;
