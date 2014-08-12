/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var OuterView = React.createClass({
  propTypes: {
    header: React.PropTypes.component
  },

  render: function() {
    return (
      <div className="content content-outer transparent ie-layout rounded">
        <div id="contentwrapper">
          {this.renderHeader()}
          <hr />
          {this.props.children}
        </div>
      </div>
    );
  },

  renderHeader: function() {
    return this.props.header || <div className="logo-small"></div>;
  }
});

module.exports = OuterView;
