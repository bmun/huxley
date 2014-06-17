/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var RRouter = require('rrouter');

var OuterView = require('./OuterView');

var RedirectView = React.createClass({
  mixins: [RRouter.RoutingContextMixin],

  componentDidMount: function() {
    if (this.props.user.isAnonymous()) {
      this.navigate('/www/login');
    } else if (this.props.user.isAdvisor()) {
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
