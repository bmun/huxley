/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var TextInput = require('components/TextInput');

var NumberInput = React.createClass({

  propTypes: {
    onChange: React.PropTypes.func,
    value: React.PropTypes.string,
    placeholder: React.PropTypes.string,
  },

  render: function() {
    return (
      <TextInput
        {...this.props}
        isControlled={true}
        onChange={this._handleChange}
      />
    );
  },

  _handleChange: function(value) {
    this.props.onChange && this.props.onChange(value.replace(/[^\d]/, ''));
  },
});

module.exports = NumberInput;
