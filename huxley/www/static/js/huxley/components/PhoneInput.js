/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react/addons');

var formatPhone = require('../utils/formatPhone');

var PhoneInput = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    value: React.PropTypes.string,
    isInternational: React.PropTypes.bool.isRequired,
  },

  componentDidUpdate: function(prevProps, prevState) {
    if (prevProps.isInternational !== this.props.isInternational) {
      var number = this._formatValue(
        this.props.value,
        this.props.isInternational
      );
      this.props.onChange && this.props.onChange(number);
    }
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
    var number = this._formatValue(
      event.target.value,
      this.props.isInternational
    );
    this.props.onChange && this.props.onChange(number);
  },

  _formatValue: function(value, isInternational) {
    var value = value || '';
    return isInternational
      ? value.replace(/[^0-9+\(\)\-\s]/, '')
      : formatPhone(value);
  },
});

module.exports = PhoneInput;
