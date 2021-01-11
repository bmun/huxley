/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var React = require("react");

require("css/content.less");

var OuterView = React.createClass({
  propTypes: {
    header: React.PropTypes.element,
  },

  render: function () {
=======
import React from "react";

require("css/content.less");

class OuterView extends React.Component {
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <div className="content content-outer transparent ie-layout rounded">
        {this.renderHeader()}
        <hr />
        {this.props.children}
      </div>
    );
  }

<<<<<<< HEAD
  renderHeader: function () {
=======
  renderHeader() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return this.props.header || <div className="logo-small" />;
  }
}

OuterView.propTypes = {
  header: React.PropTypes.element,
};

module.exports = OuterView;
