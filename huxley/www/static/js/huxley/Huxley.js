/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');
var RRouter = require('rrouter');
var CurrentUserStore = require('./stores/CurrentUserStore');

var cloneWithProps = React.addons.cloneWithProps;

var Huxley = React.createClass({
  mixins: [RRouter.RoutingContextMixin],

  componentWillMount: function() {
    CurrentUserStore.addChangeListener(function() {
      var user = CurrentUserStore.getCurrentUser();
      if (user.isAnonymous()) {
        this.navigate('/www/login');
      } else if (user.isAdvisor()) {
        this.navigate('/www/advisor/profile');
      }
    }.bind(this));
  },

  render: function() {
    return cloneWithProps(this.props.view, {
      user: CurrentUserStore.getCurrentUser()
    });
  }
});

module.exports = Huxley;
