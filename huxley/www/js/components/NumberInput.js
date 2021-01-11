/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

<<<<<<< HEAD
var React = require("react");
var TextInput = require("components/core/TextInput");

var NumberInput = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    value: React.PropTypes.string,
    placeholder: React.PropTypes.string,
  },

  render: function () {
=======
import React from "react";
var TextInput = require("components/core/TextInput");

class NumberInput extends React.Component {
  render() {
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e
    return (
      <TextInput
        {...this.props}
        isControlled={true}
        onChange={this._handleChange}
      />
    );
  }

  _handleChange(value) {
    this.props.onChange && this.props.onChange(value.replace(/[^\d]/, ""));
  }
}

<<<<<<< HEAD
  _handleChange: function (value) {
    this.props.onChange && this.props.onChange(value.replace(/[^\d]/, ""));
  },
});
=======
NumberInput.propTypes = {
  onChange: React.PropTypes.func,
  value: React.PropTypes.string,
  placeholder: React.PropTypes.string,
};
>>>>>>> 6a6c5f85d0f9eb211f9f4386f72086cbace5df4e

module.exports = NumberInput;
