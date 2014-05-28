/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var Link = require('react-router-component').Link;
var React = require('react/addons');

var OuterView = require('./OuterView');

var RegistrationView = React.createClass({
  render: function() {
    return (
      <OuterView>
        <p>Registration is coming soon!</p>
        <Link
          className="outer-nav arrow-left"
          href="/login">
          Back to Login
        </Link>
      </OuterView>
    );
  }
});

module.exports = RegistrationView;
