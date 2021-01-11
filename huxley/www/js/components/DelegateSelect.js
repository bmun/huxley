/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

class DelegateSelect extends React.Component {
  render() {
    return (
      <select
        onChange={this.props.onChange}
        value={this.props.selectedDelegateID}
        disabled={this.props.disabled}
      >
        <option value="0">None</option>
        {this.renderDelegateOptions()}
      </select>
    );
  }

  renderDelegateOptions() {
    return this.props.delegates.map((delegate) => (
      <option
        key={delegate.id}
        value={delegate.id}
        disabled={delegate.assignment}
      >
        {delegate.name}
      </option>
    ));
  }
}

DelegateSelect.propTypes = {
  onChange: React.PropTypes.func,
  delegates: React.PropTypes.array,
  selectedDelegateID: React.PropTypes.number,
  disabled: React.PropTypes.bool,
};

module.exports = DelegateSelect;
