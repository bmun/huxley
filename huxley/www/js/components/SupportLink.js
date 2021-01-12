/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

require("css/SupportLink.less");

class SupportLink extends React.Component {
  render() {
    return (
      <div className="link-wrapper">
        <span className="grey-text">Having Issues?</span>
        &nbsp; &nbsp;
        <span>
          <a
            className="mailto-link"
            href="mailto:tech@bmun.org?subject=Issues%20With%20Huxley"
          >
            Email Us
          </a>
        </span>
      </div>
    );
  }
}

export {SupportLink};
