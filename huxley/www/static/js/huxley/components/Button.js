/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');
var RRouter = require('rrouter');

var Button = React.createClass({
  propTypes: {
    color: React.PropTypes.oneOf(['blue', 'green', 'yellow']),
    href: React.PropTypes.string,
    loading: React.PropTypes.bool
  },

  render: function() {
    var cx = React.addons.classSet;
    var ButtonComponent = this.props.href ? RRouter.Link : React.DOM.button;

    return this.transferPropsTo(
      <ButtonComponent
        className={cx({
          'button': true,
          'button-blue': this.props.color == 'blue',
          'button-green': this.props.color == 'green',
          'button-yellow': this.props.color == 'yellow',
          'rounded-small': true,
          'loading': this.props.loading
        })}>
        <span>{this.props.children}</span>
      </ButtonComponent>
    );
  }
});

module.exports = Button;
