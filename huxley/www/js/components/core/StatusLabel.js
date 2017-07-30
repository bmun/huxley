/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var cx = require('classnames');

require('css/StatusLabel.less');

var StatusLabel = React.createClass({
  propTypes: {
    status: React.PropTypes.oneOf(['success', 'error']).isRequired,
  },

  render() {
    return (
      <label
        className={cx({
          'status-label': true,
          'label-success': this.props.status === 'success',
          'label-error': this.props.status === 'error',
        })}>
        {this.props.children}
      </label>
    );
  },
});

module.exports = StatusLabel;
