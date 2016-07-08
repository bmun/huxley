/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var classNames = require('classnames');
var React = require('react');
var Router = require('react-router');

var Button = React.createClass({
  propTypes: {
    color: React.PropTypes.oneOf(['blue', 'green', 'yellow', 'red']),
    href: React.PropTypes.string,
    loading: React.PropTypes.bool,
    size: React.PropTypes.oneOf(['small', 'medium', 'large']),
  },

  getDefaultProps: function() {
    return {
      color: 'blue',
      loading: false,
      size: 'medium',
    };
  },

  render: function() {
    var ButtonComponent = this.props.href ? Router.Link : 'button';

    return (
      <ButtonComponent
        {...this.props}
        className={classNames({
          'button': true,
          'button-small': this.props.size == 'small',
          'button-large': this.props.size == 'large',
          'button-blue': this.props.color == 'blue',
          'button-green': this.props.color == 'green',
          'button-yellow': this.props.color == 'yellow',
          'button-red': this.props.color == 'red',
          'rounded-small': true,
          'loading': this.props.loading
        })}
        disabled={this.props.loading}
        to={this.props.href}>
        <span>{this.props.children}</span>
      </ButtonComponent>
    );
  }
});

module.exports = Button;
