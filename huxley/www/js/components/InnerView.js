/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var React = require("react");

require("css/content.less");

var InnerView = React.createClass({
  render: function () {
=======
import React from "react";

require("css/content.less");

class InnerView extends React.Component {
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <div className="content transparent ie-layout rounded-bottom">
        {this.props.children}
      </div>
    );
  }
}

module.exports = InnerView;
