/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

require("css/content.less");

class OuterView extends React.Component {
  render() {
    return (
      <div className="content content-outer transparent ie-layout rounded">
        {this.renderHeader()}
        <hr />
        {this.props.children}
      </div>
    );
  }

  renderHeader() {
    return this.props.header || <div className="logo-small" />;
  }
}

OuterView.propTypes = {
  header: React.PropTypes.element,
};

module.exports = OuterView;
