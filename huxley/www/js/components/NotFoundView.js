/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var React = require("react");
var ReactRouter = require("react-router");

var OuterView = require("components/OuterView");

var NotFoundView = React.createClass({
  render: function () {
=======
import React from "react";

var OuterView = require("components/OuterView");

class NotFoundView extends React.Component {
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <OuterView>
        <h1>Page Not Found</h1>
        <p>
          The page you are looking for does not exist. Please return to the page
          you came from.
        </p>
      </OuterView>
    );
  }
}

module.exports = NotFoundView;
