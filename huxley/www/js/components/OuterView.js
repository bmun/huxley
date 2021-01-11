/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

var React = require("react");

require("css/content.less");

var OuterView = React.createClass({
  propTypes: {
    header: React.PropTypes.element,
  },

  render: function () {
    return (
      <div className="content content-outer transparent ie-layout rounded">
        {this.renderHeader()}
        <hr />
        {this.props.children}
      </div>
    );
  },

  renderHeader: function () {
    return this.props.header || <div className="logo-small" />;
  },
});

module.exports = OuterView;
