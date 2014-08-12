/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var RRouter = require('rrouter');

var User = require('../User');

var InnerView = React.createClass({
  componentWillMount: function() {
    if (User.isAnonymous) {
      this.navigate('www/login');
    }
  },

  render: function() {
    return (
      <div>
        <TopBar user={this.props.user} />
        <div id="appnavbar" className="titlebar rounded-top" />
        <div className="content transparent ie-layout rounded-bottom">
          <div id="contentwrapper">
            {this.props.children}
          </div>
        </div>
      </div>
    );
  },
});

module.exports = InnerView;
