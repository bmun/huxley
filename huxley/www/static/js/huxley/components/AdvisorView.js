/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var Router = require('react-router');

var NavTab = require('./NavTab');
var PermissionDeniedView = require('./PermissionDeniedView');
var TopBar = require('./TopBar');

var AdvisorView = React.createClass ({
  mixins: [Router.Navigation],

  componentDidMount: function() {
    if (this.props.user.isAnonymous()) {
      this.transitionTo('/login');
    }
  },

  render: function() {
    var content = this.props.user.isAdvisor()
      ? this.props.children
      : <PermissionDeniedView />;

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
        {this.props.children}
      </div>
    );
  },
});

module.exports = AdvisorView;
