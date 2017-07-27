/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

var React = require("react");

var PhoneInput = require("components/PhoneInput");
var StatusLabel = require("components/core/StatusLabel");

const RegistrationPhoneInput = React.createClass({
  propTypes: {
    errors: React.PropTypes.arrayOf(React.PropTypes.string),
    onChange: React.PropTypes.func,
    placeholder: React.PropTypes.string,
    value: React.PropTypes.string,
  },

  shouldComponentUpdate: function(nextProps, nextState) {
    return this.props.value !== nextProps.value;
  },

  render() {
    const {errors, ...inputProps} = this.props;
    return (
      <div className="reg-field">
        <PhoneInput {...inputProps} />
        {errors &&
          errors.map(error =>
            <StatusLabel status="error">
              {error}
            </StatusLabel>,
          )}
      </div>
    );
  },
});

module.exports = RegistrationPhoneInput;
