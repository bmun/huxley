/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var cx = require("classnames");
var Link = require("react-router").Link;
var React = require("react");

require("css/NavLink.less");

var NavLink = React.createClass({
  propTypes: {
    direction: React.PropTypes.oneOf(["left", "right"]).isRequired,
    href: React.PropTypes.string.isRequired,
  },

  render: function () {
=======
import cx from "classnames";
var Link = require("react-router").Link;
import React from "react";

require("css/NavLink.less");

class NavLink extends React.Component {
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <Link
        className={cx({
          "nav-link": true,
          "arrow-left": this.props.direction == "left",
          "arrow-right": this.props.direction == "right",
        })}
        to={this.props.href}
      >
        {this.props.children}
      </Link>
    );
  }
}

NavLink.propTypes = {
  direction: React.PropTypes.oneOf(["left", "right"]).isRequired,
  href: React.PropTypes.string.isRequired,
};
module.exports = NavLink;
