/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var NavTab = require('components/NavTab');
var PermissionDeniedView = require('components/PermissionDeniedView');
var TopBar = require('components/TopBar');
var User = require('utils/User');

var ChairView = React.createClass ({
  mixins: [ReactRouter.History],

  render: function() {
    return (
      <div>
        <TopBar user={this.props.user} />
        <div className="navbar rounded-top">
          <NavTab href="/chair/attendance">
            Attendance
          </NavTab>
        </div>
        {this.props.children}
      </div>
    );
  },
});

module.exports = ChairView;
