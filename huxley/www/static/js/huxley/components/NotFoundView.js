/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var Router = require('react-router');

var OuterView = require('./OuterView');

var NotFoundView = React.createClass ({
  render: function() {
    return (
      <OuterView>
        <h1>Page Not Found</h1>
        <p>The page you are looking for does not exist. Please return to the
        page you came from.</p>
      </OuterView>
    );
  }
});

module.exports = NotFoundView;
