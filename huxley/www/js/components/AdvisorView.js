/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import { history } from "utils/history";

var { NavTab } = require("components/NavTab");
var { PermissionDeniedView } = require("components/PermissionDeniedView");
var { Shaker } = require("components/Shaker");
var { TopBar } = require("components/TopBar");
var { User } = require("utils/User");

require("css/NavBar.less");

class AdvisorView extends React.Component {
  componentDidMount() {
    if (User.isAnonymous(this.props.user)) {
      history.redirect("/login");
    }
  }

  render() {
    var content = User.isAdvisor(this.props.user) ? (
      this.props.children
    ) : (
      <PermissionDeniedView />
    );

    return (
      <div>
        <TopBar user={this.props.user} />
        <Shaker>
          <div className="navbar rounded-top">
            <NavTab href="/advisor/profile">Profile</NavTab>
            <NavTab href="/advisor/assignments">Assignments</NavTab>
            <NavTab href="/advisor/roster">Delegates</NavTab>
            <NavTab href="/advisor/papers">Position Papers</NavTab>
            <NavTab href="/advisor/zoom-links">Zoom Links</NavTab>
            <NavTab href="/advisor/feedback">Feedback</NavTab>
          </div>
          {this.props.children}
        </Shaker>
      </div>
    );
  }
}

export { AdvisorView };
