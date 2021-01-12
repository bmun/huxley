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
var TextTemplate = require("components/core/TextTemplate");

require("css/Letter.less");
var RegistrationSuccessViewText = require("text/RegistrationSuccessViewText.md");

class RegistrationSuccessView extends React.Component {
  render() {
    var conference = this.context.conference;
    return (
      <OuterView>
        <div class="letter">
          <TextTemplate
            conferenceSession={conference.session}
            conferenceRegistrationFee={conference.registration_fee}
            conferenceDelegateFee={conference.delegate_fee}
            conferenceExternal={conference.external}
          >
            {RegistrationSuccessViewText}
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

RegistrationSuccessView.contextTypes = {
  conference: PropTypes.shape(ConferenceContext),
};


