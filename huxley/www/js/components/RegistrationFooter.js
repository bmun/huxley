/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var Button = require('components/Button');
var NavLink = require('components/NavLink');

const RegistrationFooter = React.createClass({
  propTypes: {
    loading: React.PropTypes.bool,
  },

  render: function() {
    return (
      <div id='registration_footer'>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
        <div style={{float: 'right'}}>
          <span className="help-text"><em>All done?</em></span>
          <Button
            color="green"
            loading={this.props.loading}
            type="submit">
            Register
          </Button>
        </div>
      </div>
    );
  },

});


module.exports = RegistrationFooter;
