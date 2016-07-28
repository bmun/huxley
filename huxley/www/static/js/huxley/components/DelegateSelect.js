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
    selectedDelegateId: React.PropTypes.number
  },

  render: function() {
    return (
      <select
        onChange={this.props.onChange}
        value={this.props.selectedDelegateId}>
        <option value="0">None</option>
        {this.renderDelegateOptions()}
      </select>
    );
  },

  renderDelegateOptions: function() {
    return this.props.delegates.map(function(delegate) {
      return (
        <option key={delegate.id} value={delegate.id} disabled={delegate.assignment}>
          {delegate.name}
        </option>
      );
    }.bind(this));
  }
});

module.exports = DelegateSelect;
