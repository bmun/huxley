/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var RRouter = require('rrouter');
var CurrentUserStore = require('./stores/CurrentUserStore');


var Huxley = React.createClass({
  mixins: [RRouter.RoutingContextMixin],

  componentWillMount: function() {
    CurrentUserStore.addChangeListener(function() {
      if (!CurrentUserStore.isUserLoggedIn()) {
        this.navigate('/www/login');
      } else if (CurrentUserStore.isUserAdvisor()) {
        this.navigate('/www/advisor/profile');
      }
    }.bind(this));
  },

  render: function() {
    return this.props.view;
  }
});

module.exports = Huxley;
