/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react/addons');
var Router = require('react-router');

var AdvisorView = require('../components/AdvisorView');
var CurrentUserStore = require('../stores/CurrentUserStore');
var User = require('../utils/User');

var RouteHandler = Router.RouteHandler;

var Huxley = React.createClass({
  mixins: [Router.Navigation],

  childContextTypes: {
    session: React.PropTypes.number,
    startDate: React.PropTypes.string,
    endDate: React.PropTypes.string
  },

  getChildContext: function() {
    var conference = global.conference;
    delete global.conference;
    return {
      session: conference['session'],
      startDate: conference['start_date'],
      endDate: conference['end_date']
    }
  },

  componentWillMount: function() {
    CurrentUserStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      if (User.isAnonymous(user)) {
        this.transitionTo('/login');
      } else if (User.isAdvisor(user)) {
        this.transitionTo('/advisor/profile');
      }
    });
  },

  render: function() {
    var user = CurrentUserStore.getCurrentUser();
    if (User.isAnonymous(user)) {
      return <RouteHandler user={user} />;
    } else if (User.isAdvisor(user)) {
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
