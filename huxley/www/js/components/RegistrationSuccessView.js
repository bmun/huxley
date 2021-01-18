/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var {ConferenceContext} = require("components/ConferenceContext");
var {NavLink} = require("components/NavLink");
var {OuterView} = require("components/OuterView");
var {TextTemplate} = require("components/core/TextTemplate");

require("css/Letter.less");
var RegistrationSuccessViewText = require("text/RegistrationSuccessViewText.md");

class RegistrationSuccessView extends React.Component {
  render() {
    return (
      <OuterView>
        <div class="letter">
          <TextTemplate
            conferenceSession={global.conference.session}
            conferenceRegistrationFee={global.conference.registration_fee}
            conferenceDelegateFee={global.conference.delegate_fee}
            conferenceExternal={global.conference.external}
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

export {RegistrationSuccessView};
