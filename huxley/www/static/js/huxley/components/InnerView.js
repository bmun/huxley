/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');

var InnerView = React.createClass({
  render: function() {
    // TODO: header, change password, navigation bar.
    return (
      <div className="content transparent ie-layout rounded-bottom">
        <div id="contentwrapper">
          {this.props.children}
        </div>
      </div>
    );
  }
});

module.exports = InnerView;
