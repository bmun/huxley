/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var cx = require('classnames');
var Link = require('react-router').Link;
var React = require('react');

require('css/NavLink.less');

var NavLink = React.createClass({
  propTypes: {
    direction: React.PropTypes.oneOf(['left', 'right']).isRequired,
    href: React.PropTypes.string.isRequired,
  },

  render: function() {
    return (
      <Link
        className={cx({
          'nav-link': true,
          'arrow-left': this.props.direction == 'left',
          'arrow-right': this.props.direction == 'right',
        })}
        to={this.props.href}>
        {this.props.children}
      </Link>
    );
  },
});

module.exports = NavLink;
