/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var {ConferenceContext} = require("components/ConferenceContext");
var NavLink = require("components/NavLink");
var OuterView = require("components/OuterView");
var {TextTemplate} = require("components/core/TextTemplate");

require("css/Letter.less");
var RegistrationWaitlistViewText = require("text/RegistrationWaitlistViewText.md");

class RegistrationWaitlistView extends React.Component {
  render() {
    var conference = this.context.conference;
    return (
      <OuterView>
        <div class="letter">
          <TextTemplate conferenceSession={conference.session}>
            {RegistrationWaitlistViewText}
          </TextTemplate>
        </div>
        <hr />
        <NavLink direction="right" href="/login">
          Proceed to Login
        </NavLink>
      </OuterView>
    );
  }
}

RegistrationWaitlistView.contextTypes = {
  conference: PropTypes.shape(ConferenceContext),
};


