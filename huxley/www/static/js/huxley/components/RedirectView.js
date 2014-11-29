/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var Router = require('react-router');

var OuterView = require('./OuterView');

var RedirectView = React.createClass({
  mixins: [Router.Navigation],

  componentDidMount: function() {
    if (this.props.user.isAnonymous()) {
      this.transitionTo('/login');
    } else if (this.props.user.isAdvisor()) {
      this.transitionTo('/advisor/profile');
    }
  },

  render: function() {
    // TODO: make this the same component as the loading indicator... when the
    // loading indicator is actually built.
    return <OuterView />;
  }
});

module.exports = RedirectView;
