/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var TextInput = require('components/TextInput');

var formatPhone = require('utils/formatPhone');

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
      <TextInput
        {...this.props}
        placeholder="Phone Number"
        onChange={this._handleChange}
      />
    );
  },

  _handleChange: function(value) {
    var number = this._formatValue(value, this.props.isInternational);
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
