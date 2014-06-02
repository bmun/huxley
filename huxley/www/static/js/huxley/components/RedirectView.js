/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var RRouter = require('rrouter');

var CurrentUserStore = require('../stores/CurrentUserStore');
var OuterView = require('./OuterView');

var RedirectView = React.createClass({
  mixins: [RRouter.RoutingContextMixin],

  componentWillMount: function() {
    if (!CurrentUserStore.isUserLoggedIn()) {
      this.navigate('/www/login');
    } else if (CurrentUserStore.isUserAdvisor()) {
      this.navigate('/www/advisor/profile');
    }
  },

  render: function() {
    // TODO: make this the same component as the loading indicator... when the
    // loading indicator is actually built.
    return <OuterView />;
  }
});

module.exports = RedirectView;
