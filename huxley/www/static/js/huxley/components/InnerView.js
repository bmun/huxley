/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var TopBar = require('./TopBar');

var InnerView = React.createClass({
  render: function() {
    return (
      <div>
        <TopBar user={this.props.user} />
        <div id="appnavbar" className="titlebar rounded-top" />
        <div className="content transparent ie-layout rounded-bottom">
          {this.props.children}
        </div>
      </div>
    );
  },
});

module.exports = InnerView;
