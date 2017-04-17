/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var cx = require('classnames');
var React = require('react');
var ReactRouter = require('react-router');

var Button = React.createClass({
  propTypes: {
    color: React.PropTypes.oneOf(['blue', 'green', 'yellow', 'red']),
    href: React.PropTypes.string,
    loading: React.PropTypes.bool,
    size: React.PropTypes.oneOf(['small', 'medium', 'large']),
    success: React.PropTypes.bool
  },

  getDefaultProps: function() {
    return {
      color: 'blue',
      loading: false,
      size: 'medium',
      success: false,
    };
  },

  render: function() {
    var ButtonComponent = this.props.href ? ReactRouter.Link : 'button';

    return (
      <ButtonComponent
        {...this.props}
        className={cx({
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
        {this.props.success ?
          <div className="checkmark-circle">
            <div className="background"></div>
            <div className="checkmark draw"></div>
          </div> :
          <span>{this.props.children}</span>
        }
      </ButtonComponent>
    );
  }
});

module.exports = Button;
