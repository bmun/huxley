/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import React from 'react';

var PhoneInput = require('components/PhoneInput');
var StatusLabel = require('components/core/StatusLabel');

class RegistrationPhoneInput extends React.Component {
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
  }
};

RegistrationPhoneInput.propTypes = {
  errors: React.PropTypes.arrayOf(React.PropTypes.string),
  onChange: React.PropTypes.func,
  placeholder: React.PropTypes.string,
  value: React.PropTypes.string,
}

module.exports = RegistrationPhoneInput;
