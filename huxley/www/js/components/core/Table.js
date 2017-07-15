/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

const React = require('react');
const cx = require('classnames');

require('css/Table.less');

const Table = React.createClass({
  propTypes: {
    emptyMessage: React.PropTypes.string.isRequired,
    isEmpty: React.PropTypes.bool.isRequired,
  },

  render() {
    const {emptyMessage, isEmpty, children} = this.props;
    return (
      <div className="table-container">
        <table>
          {this.props.children}
        </table>
        {isEmpty ? <div className="empty help-text">{emptyMessage}</div> : null}
      </div>
    );
  },
});

module.exports = Table;
