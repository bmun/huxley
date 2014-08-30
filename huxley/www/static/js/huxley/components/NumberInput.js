/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react')

var NumberInput = React.createClass({

  render: function() {
    return (
      <input
        type="text"
        placeholder={this.props.placeholder}
        onChange={this._handleChange}
        value={this.props.value}
      />
    );
  },

  _handleChange: function(event) {
    var value = event.target.value.replace(/[^0-9]/, '') || '';
    this.props.onChange && this.props.onChange(value);
  },
});

module.exports = NumberInput;
