/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react/addons');
var Router = require('react-router');

var AdvisorView = require('./components/AdvisorView');
var CurrentUserStore = require('./stores/CurrentUserStore');

var RouteHandler = Router.RouteHandler;

var Huxley = React.createClass({
  mixins: [Router.Navigation],

  componentWillMount: function() {
    CurrentUserStore.addChangeListener(function() {
      var user = CurrentUserStore.getCurrentUser();
      if (user.isAnonymous()) {
        this.transitionTo('/login');
      } else if (user.isAdvisor()) {
        this.transitionTo('/advisor/profile');
      }
    }.bind(this));
  },

  render: function() {
    var user = CurrentUserStore.getCurrentUser();
    if (user.isAnonymous()) {
      return <RouteHandler user={user} />;
    } else if (user.isAdvisor()) {
      return (
        <AdvisorView user={user}>
          <RouteHandler user={user} />
        </AdvisorView>
      );
    } else {
      // TODO: Chairs
    }
  },
});

module.exports = Huxley;
