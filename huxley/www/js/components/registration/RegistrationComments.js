/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from 'prop-types';

class RegistrationComments extends React.Component {
  shouldComponentUpdate(nextProps, nextState) {
    return this.props.value !== nextProps.value;
  }
  render() {
    return (
      <div id="comments">
        <h3>Comments</h3>
        <p className="instructions">
          If there are any further details you would like us to know about your
          participation in BMUN this year or general feedback about the
          registration process, please comment below.
        </p>
        <textarea
          className="text-input"
          cols="40"
          rows="7"
          onChange={this.props.handler}
          value={this.props.value}
        />
      </div>
    );
  }
}

RegistrationComments.propTypes = {
  handler: PropTypes.func,
  value: PropTypes.string,
};

module.exports = RegistrationComments;
