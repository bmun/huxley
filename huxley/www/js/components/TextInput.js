/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var cx = require('classnames');

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
    if (!this.props.isControlled) {
      return (
        <input
          defaultValue={this.props.defaultValue || ''}
          onChange={this.props.onChange}
          placeholder={this.props.placeholder}
          className={cx('text-input', this.props.className)}
          type={this.props.type || 'text'}
          onChange={this._handleChange}
        />
      );
    } else {
      return (
        <input
          {...this.props}
          className={cx('text-input', this.props.className)}
          type={this.props.type || 'text'}
          onChange={this._handleChange}
        />
      );
    }
  },

  _handleChange: function(event) {
    this.props.onChange && this.props.onChange(event.target.value);
  },
});

module.exports = TextInput;
