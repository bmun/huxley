/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');

var PermissionDeniedView = React.createClass({
  render: function(){
    <h2>Permission Denied</h2>
    <p>We are sorry but you do not have permission to view this page. Please
    press the back button on your browser or email Tech@bmun.org if you feel
    that you have encountered this message in error.</p>
  }
});

module.exports = PermissionDeniedView;
