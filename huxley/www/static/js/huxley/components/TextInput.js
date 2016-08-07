/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react')

var TextInput = React.createClass({

  propTypes: {
    onChange: React.PropTypes.func,
    placeholder: React.PropTypes.string,
    value: React.PropTypes.string,
    type: React.PropTypes.oneOf(['text', 'password']),
  },

  render: function() {
    return (
      <input
        {...this.props}
        type={this.props.type || 'text'}
        onChange={this._handleChange}
      />
    );
  },

  _handleChange: function(event) {
    this.props.onChange && this.props.onChange(event.target.value);
  },
});

module.exports = TextInput;
