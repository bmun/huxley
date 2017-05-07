/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var ReactDOM = require('react-dom');

var cx = require('classnames');

require('css/Shaker.less');

var Shaker = React.createClass({
  childContextTypes: {
    shake: React.PropTypes.func,
  },

  getChildContext() {
    return {
      shake: this.shake,
    };
  },

  render() {
    return (
      <div className={cx('shaker', this.props.className)}>
        {this.props.children}
      </div>
    );
  },

  shake() {
    const element = ReactDOM.findDOMNode(this);
    if (element) {
      this._timeout && clearTimeout(this._timeout);
      element.classList.remove('shake');
      element.classList.add('shake');
      this._timeout = setTimeout(() => {
        element.classList.remove('shake');
      }, 301);
    }
  },
});

module.exports = Shaker;
