/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var AdvisorView = require('components/AdvisorView');
var ChairView = require('components/ChairView');
var ConferenceContext = require('components/ConferenceContext');
var CurrentUserStore = require('stores/CurrentUserStore');
var User = require('utils/User');

require('css/base.less');
require('css/Banner.less');
require('css/JSWarning.less');
require('css/IEWarning.less');

var Huxley = React.createClass({
  mixins: [ReactRouter.History,],

  childContextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getChildContext: function() {
    var conference = global.conference;
    return {
      conference: conference
    };
  },

  componentWillMount: function() {
    CurrentUserStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      if (User.isAnonymous(user)) {
        this.history.pushState(null, '/login');
      } else if (User.isAdvisor(user)) {
        this.history.pushState(null, '/advisor/profile');
      } else if (User.isChair(user)) {
        this.history.pushState(null, '/chair/attendance');
      }
    });
  },

  render: function() {
    var user = CurrentUserStore.getCurrentUser();
    if (User.isAnonymous(user)) {
      return React.cloneElement(this.props.children, { user: user });
    } else if (User.isAdvisor(user)) {
      return (
        <AdvisorView user={user}>
          {React.cloneElement(this.props.children, { user: user })}
        </AdvisorView>
      );
    } else if (User.isChair(user)) {
      return (
        <ChairView user={user}>
          {React.cloneElement(this.props.children, { user: user })}
        </ChairView>
      );
    }
  },
});

module.exports = Huxley;
