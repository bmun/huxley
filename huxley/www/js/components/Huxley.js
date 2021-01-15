/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";
import {history} from "utils/history";

var {AdvisorView} = require("components/AdvisorView");
var {ChairView} = require("components/ChairView");
var {DelegateView} = require("components/DelegateView");
var {ConferenceContext} = require("components/ConferenceContext");
var {CurrentUserStore} = require("stores/CurrentUserStore");
var {Shaker} = require("components/Shaker");
var {SupportLink} = require("components/SupportLink");
var {User} = require("utils/User");

require("css/base.less");
require("css/Banner.less");
require("css/JSWarning.less");
require("css/IEWarning.less");

class Huxley extends React.Component {
  componentWillMount() {
    CurrentUserStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      console.log(user);
      if (User.isAnonymous(user)) {
        history.redirect("/login");
      } else if (User.isAdvisor(user)) {
        history.redirect("/advisor/profile");
      } else if (User.isChair(user)) {
        history.redirect("/chair/attendance");
      } else if (User.isDelegate(user)) {
        history.redirect("/delegate/profile");
      }
    });
  }

  render() {
    var user = CurrentUserStore.getCurrentUser();
    if (User.isAnonymous(user)) {
      return (
        <div>
          <Shaker>
            {React.cloneElement(this.props.children, { user: user })}
          </Shaker>
          <SupportLink />
        </div>
      );
    } else if (User.isAdvisor(user)) {
      return (
        <div>
          <AdvisorView user={user}>
            {React.cloneElement(this.props.children, { user: user })}
          </AdvisorView>
          <SupportLink />
        </div>
      );
    } else if (User.isChair(user)) {
      return (
        <div>
          <ChairView user={user}>
            {React.cloneElement(this.props.children, { user: user })}
          </ChairView>
          <SupportLink />
        </div>
      );
    } else if (User.isDelegate(user)) {
      return (
        <div>
          <DelegateView user={user}>
            {React.cloneElement(this.props.children, { user: user })}
          </DelegateView>
          <SupportLink />
        </div>
      );
    }
  }
}

export {Huxley};
