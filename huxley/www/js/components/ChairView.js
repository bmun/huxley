/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NavTab = require('components/NavTab');
var Shaker = require('components/Shaker');
var TopBar = require('components/TopBar');

require('css/NavBar.less');

var ChairView = React.createClass({
  render() {
    return (
      <div>
        <TopBar user={this.props.user} />
        <Shaker>
          <div className="navbar rounded-top">
            <NavTab href="/chair/rubric">Rubric</NavTab>
            <NavTab href="/chair/papers">Papers</NavTab>
            <NavTab href="/chair/attendance">Attendance</NavTab>
            <NavTab href="/chair/summary">Summaries</NavTab>
            <NavTab href="/chair/committee_feedback">Committee Feedback</NavTab>
            <NavTab href="chair/delegate_emails">Delegate Emails</NavTab>
          </div>
          {this.props.children}
        </Shaker>
      </div>
    );
  },
});

module.exports = ChairView;
