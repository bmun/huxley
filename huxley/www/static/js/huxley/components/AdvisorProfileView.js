/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var CurrentUserActions = require('../actions/CurrentUserActions');
var InnerView = require('./InnerView');
var LogoutButton = require('./LogoutButton');

var AdvisorProfileView = React.createClass({
  render: function() {
    return (
      <InnerView>
        <p>This is the advisor profile view. It does not do anything yet.</p>
        <LogoutButton />
      </InnerView>
    );
  },
});

module.exports = AdvisorProfileView;
