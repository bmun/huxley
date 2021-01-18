/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import {history} from "utils/history";

var {CurrentUserStore} = require("stores/CurrentUserStore");
var {OuterView} = require("components/OuterView");
var {User} = require("utils/User");

class RedirectView extends React.Component {
  componentDidMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (User.isAnonymous(user)) {
      history.redirect("/login");
    } else if (User.isAdvisor(user)) {
      history.redirect("/advisor/profile");
    } else if (User.isChair(user)) {
      history.redirect("/chair/attendance");
    } else if (User.isDelegate(user)) {
      history.redirect("/delegate/profile");
    }
  }

  render() {
    // TODO: make this the same component as the loading indicator... when the
    // loading indicator is actually built.
    return <OuterView />;
  }
}

export {RedirectView};
