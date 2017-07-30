/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var cx = require('classnames');

require('css/TextInput.less');

/**
 * TextInput is uncontrolled by default to preserve cursor position.
 * Controlled inputs cannot preserve cursor position upon rendering.
 * See issue #519.
 */
var TextInput = React.createClass({
  propTypes: {
    defaultValue: React.PropTypes.string,
    isControlled: React.PropTypes.bool,
    onChange: React.PropTypes.func,
    placeholder: React.PropTypes.string,
    value: React.PropTypes.string,
    type: React.PropTypes.oneOf(['text', 'password']),
  },

  render: function() {
    return (
      <input
        {...this.props}
        className={cx('text-input', this.props.className)}
        onChange={this._handleChange}
        type={this.props.type || 'text'}
        value={this.props.isControlled ? this.props.value : undefined}
      />
    );
  },

  _handleChange: function(event) {
    this.props.onChange && this.props.onChange(event.target.value);
  },
});

module.exports = TextInput;
