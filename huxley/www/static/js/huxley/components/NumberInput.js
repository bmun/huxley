/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react')

var NumberInput = React.createClass({

  propTypes: {
    onChange: React.PropTypes.func,
    value: React.PropTypes.string,
    placeholder: React.PropTypes.string,
  },

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
    var value = event.target.value.replace(/[^\d]/, '');
    this.props.onChange && this.props.onChange(value);
  },
});

module.exports = NumberInput;
