/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NavTab = require('components/NavTab');
var TopBar = require('components/TopBar');

var ChairView = React.createClass({
  render() {
    return (
      <div>
        <TopBar user={this.props.user} />
        <div className="navbar rounded-top">
          <NavTab href="/chair/attendance">
            Attendance
          </NavTab>
          <NavTab href="/chair/summary">
            Summaries
          </NavTab>
        </div>
        {this.props.children}
      </div>
    );
  },
});

module.exports = ChairView;
