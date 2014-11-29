/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react/addons');
var Router = require('react-router');

var Button = React.createClass({
  propTypes: {
    color: React.PropTypes.oneOf(['blue', 'green', 'yellow']),
    href: React.PropTypes.string,
    loading: React.PropTypes.bool,
    size: React.PropTypes.oneOf(['small', 'medium']),
  },

  getDefaultProps: function() {
    return {
      color: 'blue',
      loading: false,
      size: 'medium',
    };
  },

  render: function() {
    var cx = React.addons.classSet;
    var ButtonComponent = this.props.href ? Router.Link : 'button';

    return (
      <ButtonComponent
        {...this.props}
        className={cx({
          'button': true,
          'button-small': this.props.size == 'small',
          'button-blue': this.props.color == 'blue',
          'button-green': this.props.color == 'green',
          'button-yellow': this.props.color == 'yellow',
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
