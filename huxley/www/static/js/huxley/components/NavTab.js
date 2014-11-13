/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var Link = require('rrouter').Link;
var React = require('react');

var NavTab = React.createClass({
  propTypes: {
    href: React.PropTypes.string.isRequired
  },

  render: function() {
    return (
      <Link href={this.props.href} className='tab'>
        {this.props.children}
      </Link>
    );
  }
});

module.exports = NavTab;
