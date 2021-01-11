/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var NavTab = require('components/NavTab');
var Shaker = require('components/Shaker');
var TopBar = require('components/TopBar');

require('css/NavBar.less');

var DelegateView = React.createClass({
  render() {
    return (
      <div>
        <TopBar user={this.props.user} />
        <Shaker>
          <div className="navbar rounded-top">
            <NavTab href="/delegate/profile">Profile</NavTab>
            <NavTab href="/delegate/paper">Paper</NavTab>
            <NavTab href="/delegate/notes">Notes</NavTab>
            <NavTab href="/delegate/committee_feedback">
              Committee Feedback
            </NavTab>
          </div>
          {this.props.children}
        </Shaker>
      </div>
    );
  },
});

module.exports = DelegateView;
