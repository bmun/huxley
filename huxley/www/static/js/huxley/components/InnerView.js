/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var InnerView = React.createClass({
  render: function() {
    return (
      <div className="content transparent ie-layout rounded-bottom">
        {this.props.children}
      </div>
    );
  },
});

module.exports = InnerView;
