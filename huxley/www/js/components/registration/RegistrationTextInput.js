/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var TextInput = require('components/core/TextInput');
var StatusLabel = require('components/core/StatusLabel');

const RegistrationTextInput = React.createClass({
  propTypes: {
    errors: React.PropTypes.arrayOf(React.PropTypes.string),
    onChange: React.PropTypes.func,
    placeholder: React.PropTypes.string,
    value: React.PropTypes.string,
    type: React.PropTypes.oneOf(['text', 'password']),
  },

  render() {
    const {errors, ...inputProps} = this.props;
    return (
      <div className="reg-field">
        <TextInput {...inputProps} />
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

module.exports = RegistrationTextInput;
