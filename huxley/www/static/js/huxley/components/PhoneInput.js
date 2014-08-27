/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var formatPhone = require('../utils/formatPhone');

var PhoneInput = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    value: React.PropTypes.string,
    isInternational: React.PropTypes.bool
  },

  render: function() {
    return (
      <input
        type="text"
        placeholder="Phone Number"
        onChange={this._handleChange}
        value={this.props.value}
      />
    );
  },

  _handleChange: function(event) {
    var value = event.target.value;
    var number = this.props.isInternational
      ? value.replace(/[^0-9+\(\)\-]/, '')
      : formatPhone(value);
    this.props.onChange(number);
  }
});

module.exports = PhoneInput;
