/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

require("css/content.less");

class InnerView extends React.Component {
  render() {
    return (
      <div className="content transparent ie-layout rounded-bottom">
        {this.props.children}
      </div>
    );
  }
}

export { InnerView };
