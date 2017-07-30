/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Link = require('react-router').Link;
var React = require('react');

var NavTab = React.createClass({
  propTypes: {
    href: React.PropTypes.string.isRequired,
  },

  render: function() {
    return (
      <Link activeClassName="current" className="tab" to={this.props.href}>
        {this.props.children}
      </Link>
    );
  },
});

module.exports = NavTab;
