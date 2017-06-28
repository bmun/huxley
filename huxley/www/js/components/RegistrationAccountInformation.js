/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var RegistrationTextInput = require('components/RegistrationTextInput');
var _accessSafe = require('utils/_accessSafe');

const RegistrationAccountInformation = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    errors: React.PropTypes.object,
    accountInformation: React.PropTypes.object,
    blur: React.PropTypes.func,
    focus: React.PropTypes.func,
  },

  shouldComponentUpdate: function(nextProps, nextState) {
    for (var key in this.props.accountInformation) {
      if (this.props.accountInformation[key] !== nextProps.accountInformation[key]) {
        return true;
      }
    }
    return false;
  },

  render: function() {
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessAccount = _accessSafe.bind(this, this.props.accountInformation);
    return (
      <div id="account_information">
        <h3>Account Information</h3>
        <RegistrationTextInput  
          errors={accessErrors('first_name')} 
          placeholder="First Name" 
          onChange={accessHandlers('first_name')} 
          value={accessAccount('first_name')} 
        />
        <RegistrationTextInput 
          errors={accessErrors('last_name')} 
          placeholder="Last Name" 
          onChange={accessHandlers('last_name')} 
          value={accessAccount('last_name')} 
        />
        <RegistrationTextInput
          errors={accessErrors('username')} 
          placeholder="Username" 
          onChange={accessHandlers('username')} 
          value={accessAccount('username')}
        />
        <RegistrationTextInput
          errors={accessErrors('password')} 
          type="password" 
          placeholder="Password" 
          value={accessAccount('password')} 
          onChange={accessHandlers('password')}
          onBlur={this.props.blur} 
          onFocus={this.props.focus} 
        />
        <RegistrationTextInput
          errors={accessErrors('password_confirm')} 
          type="password" 
          placeholder="Password (confirm)" 
          value={accessAccount('password_confirm')} 
          onChange={accessHandlers('password_confirm')} 
          onBlur={this.props.blur}
          onFocus={this.props.focus} 
        />
      </div>
    );
  },
});


module.exports = RegistrationAccountInformation;
