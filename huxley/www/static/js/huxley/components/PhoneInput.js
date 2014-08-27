/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');

var formatPhone = require('../utils/formatPhone');

var PhoneInput = React.createClass({
  render: function() {
    return(
      <input
        type="text"
        placeholder="Phone Number"
        onChange={this._handleChange}
        value={this.props.value}
      />
    );
  },

  _handleChange: function(event) {
    if(this.props.isInternational){
      return (
        this.props.onChange(event.target.value.replace(/[^0-9+\(\)\-]/, ""))
      );
    } else {
      return this.props.onChange(formatPhone(event.target.value));
    }
  }
});

module.exports = PhoneInput;
