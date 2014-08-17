/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var InnerView = require('./InnerView');
var RRouter = require('rrouter');
var PermissionDeniedView = require('./PermissionDeniedView');

var AdvisorView = React.createClass ({
  mixins: [RRouter.RoutingContextMixin],

  componentDidMount: function() {
    if (this.props.user.isAnonymous()) {
      this.navigate('/login');
    }
  },

  render: function() {
    if (this.props.user.isAdvisor()) {
      return (
        <InnerView user={this.props.user}>
          {this.props.children}
        </InnerView>
      );
    } else if (this.props.user.isChair()) {
      return (
        <InnerView user={this.props.user}>
          <PermissionDeniedView />
        </InnerView>
      );
    } else {
      return (
        <div />
      );
    }
  }
});

module.exports = AdvisorView;
