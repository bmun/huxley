/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var NavTab = require('./NavTab');
var PermissionDeniedView = require('./PermissionDeniedView');
var TopBar = require('./TopBar');
var User = require('../utils/User');

var AdvisorView = React.createClass ({
  mixins: [ReactRouter.History],

  componentDidMount: function() {
    if (User.isAnonymous(this.props.user)) {
      this.history.pushState(null, '/login');
    }
  },

  render: function() {
    var content = User.isAdvisor(this.props.user)
      ? this.props.children
      : <PermissionDeniedView />;

    return (
      <div>
        <TopBar user={this.props.user} />
        <div className="navbar rounded-top">
          <NavTab href="/advisor/profile">
            Profile
          </NavTab>
          <NavTab href="/advisor/assignments">
            Assignments
          </NavTab>
          <NavTab href="/advisor/roster">
            Delegates
          </NavTab>
        </div>
        {this.props.children}
      </div>
    );
  },
});

module.exports = AdvisorView;
