/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var PermissionDeniedView = React.createClass({
  render: function() {
    return (
      <div>
        <h2>Permission Denied</h2>
        <p>We are sorry but you do not have permission to view this page. Please
        press the back button on your browser or email
        <a href="mailto:tech@bmun.org"> tech@bmun.org</a>
        if you feelthat you have encountered this message in error.</p>
      </div>
    );
  }
});

module.exports = PermissionDeniedView;
