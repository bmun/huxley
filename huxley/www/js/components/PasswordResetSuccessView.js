/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

var React = require("react");

var NavLink = require("components/NavLink");
var OuterView = require("components/OuterView");
var TextTemplate = require("components/core/TextTemplate");

var PasswordResetSuccessViewText = require("text/PasswordResetSuccessViewText.md");

var PasswordResetSuccessView = React.createClass({
  render: function() {
    return (
      <OuterView>
        <TextTemplate>
          {PasswordResetSuccessViewText}
        </TextTemplate>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
      </OuterView>
    );
  },
});

module.exports = PasswordResetSuccessView;
