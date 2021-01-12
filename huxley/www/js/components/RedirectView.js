/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import history from "utils/history";

var OuterView = require("components/OuterView");
var User = require("utils/User");

class RedirectView extends React.Component {
  componentDidMount() {
    var { user } = this.props;
    if (User.isAnonymous(user)) {
      history.pushState(null, "/login");
    } else if (User.isAdvisor(user)) {
      history.pushState(null, "/advisor/profile");
    } else if (User.isChair(user)) {
      history.pushState(null, "/chair/attendance");
    } else if (User.isDelegate(user)) {
      history.pushState(null, "/delegate/profile");
    }
  }

  render() {
    // TODO: make this the same component as the loading indicator... when the
    // loading indicator is actually built.
    return <OuterView />;
  }
}


