/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";

var TextTemplate = require("components/core/TextTemplate");

var PermissionDeniedViewText = require("text/PermissionDeniedViewText.md");

class PermissionDeniedView extends React.Component {
  render() {
    return (
      <div>
        <TextTemplate>{PermissionDeniedViewText}</TextTemplate>
      </div>
    );
  }
}

export {PermissionDeniedView};
