/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var InnerView = require('./InnerView');
var RRouter = require('rrouter')

var User = require('User')

var AdvisorView = React.createClass ({
  mixins: [RRouter.RoutingContextMixin],

  propTypes: {
    user: React.PropTypes.instanceOf(User).isRequired
  },

  getIntialState: function() {
    return {
      authorized: false
    };
  },

  componentWillMount: function() {
    if (this.props.user.isAdvisor()) {
      this.setState({authorized: true})
    } else if (this.props.user.isAnonymous()) {
      this.navigate('www/login');
    }
  },

  render: function() {
    if (this.state.authorized){
      return(
        <InnerView user={this.props.user}>
          {this.props.children}
        </InnerView>
      );
    } else {
      return(
        <InnerView>
          <PermissionDeniedView>
            {this.props.children}
          </PermissionDeniedView>
        </InnerView>
      );
    }
  },
});

module.exports = AdvisorView;
