/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

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

  renderDelegateOptions = () => {
    return this.props.delegates.map((delegate) => (
      <option
        key={delegate.id}
        value={delegate.id}
        disabled={delegate.assignment}
      >
        {delegate.name}
      </option>
    ));
  };
}

DelegateSelect.propTypes = {
  onChange: PropTypes.func,
  delegates: PropTypes.array,
  selectedDelegateID: PropTypes.number,
  disabled: PropTypes.bool,
};

export { DelegateSelect };
