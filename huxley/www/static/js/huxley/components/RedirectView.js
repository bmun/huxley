/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var OuterView = require('./OuterView');
var User = require('../utils/User');

var RedirectView = React.createClass({
  mixins: [ReactRouter.History],

  componentDidMount: function() {
    var {user} = this.props;
    if (User.isAnonymous(user)) {
      this.history.pushState(null, '/login');
    } else if (User.isAdvisor(user)) {
      this.history.pushState(null, '/advisor/profile');
    }
  },

  render: function() {
    // TODO: make this the same component as the loading indicator... when the
    // loading indicator is actually built.
    return <OuterView />;
  }
});

module.exports = RedirectView;
