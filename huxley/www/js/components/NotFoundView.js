/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

var {OuterView} = require("components/OuterView");

class NotFoundView extends React.Component {
  render() {
    return (
      <OuterView>
        <h1>Page Not Found</h1>
        <p>
          The page you are looking for does not exist. Please return to the page
          you came from.
        </p>
      </OuterView>
    );
  }
}

export {NotFoundView};
