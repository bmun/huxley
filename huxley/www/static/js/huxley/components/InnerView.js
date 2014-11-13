/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var TopBar = require('./TopBar');
var NavTab = require('./NavTab');

var InnerView = React.createClass({
  render: function() {
    return (
      <div>
        <TopBar user={this.props.user} />
        <div id="appnavbar" className="titlebar rounded-top">
          <NavTab href="/advisor/profile">
            Profile
          </NavTab>
          <NavTab href="/advisor/assignments">
            Assignments
          </NavTab>
        </div>
        <div className="content transparent ie-layout rounded-bottom">
          {this.props.children}
        </div>
      </div>
    );
  },
});

module.exports = InnerView;
