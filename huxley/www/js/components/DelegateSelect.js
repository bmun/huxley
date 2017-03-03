/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var DelegateSelect = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    delegates: React.PropTypes.array,
    selectedDelegateID: React.PropTypes.number
  },

  render: function() {
    return (
      <select
        onChange={this.props.onChange}
        value={this.props.selectedDelegateID}
        disabled>
        <option value="0">None</option>
        {this.renderDelegateOptions()}
      </select>
    );
  },

  renderDelegateOptions: function() {
    return this.props.delegates.map((delegate) =>
      <option key={delegate.id} value={delegate.id} disabled={delegate.assignment}>
        {delegate.name}
      </option>
    );
  }
});

module.exports = DelegateSelect;
